# Port Connectivity Checker

[绠€浣撲腑鏂嘳(README.zh-CN.md)

Check whether an explicit list of TCP host and port targets is reachable, with timeouts, concurrency, and reports.

## Features

- Accepts `host:port` arguments or a text file.
- Supports bracketed IPv6, for example `[::1]:8080`.
- Configurable timeout and bounded concurrency.
- Shows resolved peer address and connection time.
- JSON and CSV reports.
- Non-zero exit status if any connection fails.

## Install

```bash
git clone https://github.com/jellywong343-sys/port-connectivity-checker.git
cd port-connectivity-checker
python -m pip install -e .
```

## Usage

```bash
port-check example.com:443 localhost:8080
port-check --file examples/targets.txt --timeout 2
port-check --file examples/targets.txt --workers 5 --json report.json --csv report.csv
```

## Responsible use

The tool checks only targets you explicitly list; it does not scan port ranges. Only test systems you own or are authorized to diagnose. Network filters can make a reachable service appear closed or timed out.

Tests use a fake socket and do not contact real hosts.

## Tests

```bash
python -m unittest discover -s tests -v
```

## License

MIT

