import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parents[1] / "src"))
from port_connectivity_checker.cli import Target, check_target, load_targets, parse_target

class FakeSocket:
    def getpeername(self): return ("203.0.113.10", 443)
    def close(self): self.closed = True

class PortCheckerTests(unittest.TestCase):
    def test_parse_ipv4_hostname_and_ipv6(self):
        self.assertEqual(parse_target("example.test:443"), Target("example.test", 443))
        self.assertEqual(parse_target("[::1]:8080"), Target("::1", 8080))
        with self.assertRaises(ValueError): parse_target("example.test:70000")

    def test_load_deduplicates_and_check_injection(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "targets.txt"
            path.write_text("example.test:443\n# note\nexample.test:443\nlocalhost:80\n", encoding="utf-8")
            self.assertEqual(len(load_targets([], str(path))), 2)
        def connector(address, timeout):
            self.assertEqual(address, ("example.test", 443))
            self.assertEqual(timeout, 2)
            return FakeSocket()
        result = check_target(Target("example.test", 443), timeout=2, connector=connector)
        self.assertTrue(result.open)
        self.assertEqual(result.resolved_address, "203.0.113.10")

if __name__ == "__main__": unittest.main()
