"""Unit tests; network probe is mocked to avoid external traffic."""
import sys
import unittest
from pathlib import Path
from unittest.mock import patch
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from monitor import validate_targets, check_service, run


class MonitorTests(unittest.TestCase):
    def test_explicit_targets(self):
        value = validate_targets([{"name": "local", "host": "127.0.0.1", "port": 8000}])
        self.assertEqual(value[0]["name"], "local")

    def test_invalid_port(self):
        for port in (0, 65536, "80", True):
            with self.subTest(port=port), self.assertRaises(ValueError):
                validate_targets([{"host": "localhost", "port": port}])

    def test_no_empty_target_list(self):
        with self.assertRaises(ValueError):
            validate_targets([])

    def test_reachable_mock(self):
        with patch("monitor.socket.create_connection") as connect:
            result = check_service("localhost", 80)
        self.assertEqual(result["status"], "reachable")
        connect.assert_called_once_with(("localhost", 80), timeout=1.0)

    def test_unreachable_mock(self):
        with patch("monitor.socket.create_connection", side_effect=ConnectionRefusedError):
            result = check_service("localhost", 80)
        self.assertEqual(result["status"], "unreachable")
        self.assertEqual(result["error"], "ConnectionRefusedError")

    def test_aggregate(self):
        targets = validate_targets([{"host":"localhost","port":80},{"host":"localhost","port":81}])
        with patch("monitor.check_service", side_effect=[
            {"host":"localhost","port":80,"status":"reachable","error":None,"latency_ms":1.0},
            {"host":"localhost","port":81,"status":"unreachable","error":"ConnectionRefusedError","latency_ms":1.0},
        ]):
            r=run(targets)
        self.assertEqual((r["total"],r["reachable"],r["unreachable"]),(2,1,1))

    def test_timeout_restrictions(self):
        with self.assertRaises(ValueError): run([],timeout=0)

if __name__ == "__main__":
    unittest.main()
