"""Small, opt-in TCP service availability monitor; standard library only."""
from __future__ import annotations

import argparse
import json
import socket
import time
from datetime import datetime, timezone
from pathlib import Path


def validate_targets(raw: object) -> list[dict]:
    """Validate an explicit user-supplied target list (no discovery/scanning)."""
    if not isinstance(raw, list) or not raw:
        raise ValueError("Targets must be a nonempty JSON list")
    if len(raw) > 30:
        raise ValueError("Maximum 30 explicitly listed targets")
    items = []
    for n, item in enumerate(raw, 1):
        if not isinstance(item, dict):
            raise ValueError(f"Target {n} must be an object")
        host, port = item.get("host"), item.get("port")
        if not isinstance(host, str) or not host or len(host) > 253 or any(c.isspace() for c in host):
            raise ValueError(f"Target {n}: invalid host")
        if type(port) is not int or not 1 <= port <= 65535:
            raise ValueError(f"Target {n}: port must be 1..65535")
        label = item.get("name", f"{host}:{port}")
        if not isinstance(label, str) or not label.strip():
            raise ValueError(f"Target {n}: invalid name")
        items.append({"name": label, "host": host, "port": port})
    return items


def check_service(host: str, port: int, timeout: float = 1.0) -> dict:
    """Check a single explicitly supplied TCP endpoint (not an HTTP health check)."""
    started = time.monotonic()
    try:
        with socket.create_connection((host, port), timeout=timeout):
            result = {"status": "reachable", "error": None}
    except (OSError, TimeoutError) as exc:
        result = {"status": "unreachable", "error": type(exc).__name__}
    elapsed_ms = round((time.monotonic() - started) * 1000, 2)
    return {"host": host, "port": port, **result, "latency_ms": elapsed_ms}


def run(targets: list[dict], timeout: float = 1.0) -> dict:
    if not 0 < timeout <= 10:
        raise ValueError("Timeout must be greater than 0 and at most 10 seconds")
    results = []
    for target in targets:
        results.append({"name": target["name"], **check_service(target["host"], target["port"], timeout)})
    return {
        "timestamp_utc": datetime.now(timezone.utc).isoformat(),
        "total": len(results),
        "reachable": sum(r["status"] == "reachable" for r in results),
        "unreachable": sum(r["status"] == "unreachable" for r in results),
        "results": results,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Check explicitly listed TCP services you own or are authorized to test")
    parser.add_argument("targets", type=Path, help="JSON file of explicit host/port targets")
    parser.add_argument("--timeout", type=float, default=1.0, help="Seconds (0 < timeout <= 10)")
    parser.add_argument("--json", type=Path, dest="output", help="Save JSON report")
    args = parser.parse_args()
    try:
        targets = validate_targets(json.loads(args.targets.read_text(encoding="utf-8")))
        report = run(targets, timeout=args.timeout)
        if args.output:
            args.output.write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    except (OSError, UnicodeError, ValueError, json.JSONDecodeError) as exc:
        parser.error(str(exc))
    print(f"Services: {report['total']} | Reachable: {report['reachable']} | Unreachable: {report['unreachable']}")
    for item in report["results"]:
        print(f"  {item['name']} ({item['host']}:{item['port']}): {item['status']} [{item['latency_ms']} ms]")
    if args.output:
        print(f"Report: {args.output}")


if __name__ == "__main__":
    main()
