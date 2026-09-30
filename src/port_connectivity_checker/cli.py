from __future__ import annotations

import argparse
import csv
import json
import socket
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from pathlib import Path

@dataclass(frozen=True)
class Target:
    host: str
    port: int

@dataclass
class CheckResult:
    host: str
    port: int
    open: bool
    elapsed_ms: float
    resolved_address: str | None
    error: str | None


def parse_target(value: str) -> Target:
    value = value.strip()
    if not value:
        raise ValueError("Empty target")
    if value.startswith("["):
        end = value.find("]")
        if end < 0 or end + 1 >= len(value) or value[end + 1] != ":":
            raise ValueError(f"IPv6 targets must use [address]:port: {value}")
        host, port_text = value[1:end], value[end + 2:]
    else:
        if value.count(":") != 1:
            raise ValueError(f"Target must use host:port: {value}")
        host, port_text = value.rsplit(":", 1)
    host = host.strip()
    if not host:
        raise ValueError("Host cannot be empty")
    try:
        port = int(port_text)
    except ValueError as exc:
        raise ValueError(f"Invalid port: {port_text}") from exc
    if not 1 <= port <= 65535:
        raise ValueError(f"Port out of range: {port}")
    return Target(host, port)


def load_targets(values: list[str], file: str | None) -> list[Target]:
    raw = list(values)
    if file:
        raw.extend(
            line.strip() for line in Path(file).read_text(encoding="utf-8").splitlines()
            if line.strip() and not line.lstrip().startswith("#")
        )
    unique = []
    seen = set()
    for value in raw:
        target = parse_target(value)
        key = (target.host.lower(), target.port)
        if key not in seen:
            seen.add(key)
            unique.append(target)
    if not unique:
        raise ValueError("No targets supplied")
    return unique


def check_target(target: Target, timeout: float = 3.0, connector=socket.create_connection) -> CheckResult:
    started = time.perf_counter()
    try:
        connection = connector((target.host, target.port), timeout=timeout)
        try:
            peer = connection.getpeername()
            address = str(peer[0]) if peer else None
        except (OSError, AttributeError, IndexError):
            address = None
        finally:
            connection.close()
        elapsed = round((time.perf_counter() - started) * 1000, 2)
        return CheckResult(target.host, target.port, True, elapsed, address, None)
    except (socket.timeout, socket.gaierror, ConnectionRefusedError, OSError) as exc:
        elapsed = round((time.perf_counter() - started) * 1000, 2)
        return CheckResult(target.host, target.port, False, elapsed, None, str(exc))


def check_many(targets: list[Target], timeout: float = 3.0, workers: int = 10) -> list[CheckResult]:
    workers = max(1, min(workers, 50, len(targets)))
    ordered: list[CheckResult | None] = [None] * len(targets)
    with ThreadPoolExecutor(max_workers=workers) as executor:
        futures = {executor.submit(check_target, target, timeout): index for index, target in enumerate(targets)}
        for future in as_completed(futures):
            ordered[futures[future]] = future.result()
    return [item for item in ordered if item is not None]


def write_csv(path: Path, results: list[CheckResult]) -> None:
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(asdict(results[0]).keys()))
        writer.writeheader()
        writer.writerows(asdict(item) for item in results)


def main() -> None:
    parser = argparse.ArgumentParser(description="Check explicit TCP host:port targets.")
    parser.add_argument("targets", nargs="*")
    parser.add_argument("--file", help="Text file with one host:port per line")
    parser.add_argument("--timeout", type=float, default=3.0)
    parser.add_argument("--workers", type=int, default=10)
    parser.add_argument("--json", dest="json_path")
    parser.add_argument("--csv", dest="csv_path")
    args = parser.parse_args()
    if args.timeout <= 0:
        parser.error("--timeout must be greater than zero")
    try:
        targets = load_targets(args.targets, args.file)
    except (ValueError, OSError) as exc:
        parser.error(str(exc))
    results = check_many(targets, args.timeout, args.workers)
    for item in results:
        marker = "OPEN" if item.open else "CLOSED"
        address = f" -> {item.resolved_address}" if item.resolved_address else ""
        print(f"{marker:6} {item.host}:{item.port}{address}  {item.elapsed_ms:.2f} ms")
        if item.error:
            print(f"       {item.error}")
    report = {"checked_at": datetime.now(timezone.utc).isoformat(), "results": [asdict(item) for item in results]}
    if args.json_path:
        Path(args.json_path).write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    if args.csv_path and results:
        write_csv(Path(args.csv_path), results)
    if any(not item.open for item in results):
        raise SystemExit(1)

if __name__ == "__main__": main()
