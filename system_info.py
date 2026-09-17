#!/usr/bin/env python3
"""Display useful local system information for IT support and troubleshooting."""

from __future__ import annotations

import argparse
import json
import platform
import socket
from typing import Any

import psutil


def bytes_to_gb(value: int) -> float:
    """Convert bytes to GiB rounded to two decimal places."""
    return round(value / (1024**3), 2)


def collect_system_info() -> dict[str, Any]:
    """Collect a small cross-platform system inventory."""
    memory = psutil.virtual_memory()

    return {
        "hostname": socket.gethostname(),
        "operating_system": platform.system(),
        "os_release": platform.release(),
        "os_version": platform.version(),
        "architecture": platform.machine(),
        "processor": platform.processor() or "Unknown",
        "physical_cpu_cores": psutil.cpu_count(logical=False),
        "logical_cpu_cores": psutil.cpu_count(logical=True),
        "ram_total_gb": bytes_to_gb(memory.total),
        "ram_available_gb": bytes_to_gb(memory.available),
        "ram_usage_percent": memory.percent,
    }


def print_human_readable(info: dict[str, Any]) -> None:
    print("SYSTEM INFORMATION")
    print("=" * 18)
    print(f"Hostname:            {info['hostname']}")
    print(f"Operating system:    {info['operating_system']} {info['os_release']}")
    print(f"Architecture:        {info['architecture']}")
    print(f"Processor:           {info['processor']}")
    print(f"Physical CPU cores:  {info['physical_cpu_cores']}")
    print(f"Logical CPU cores:   {info['logical_cpu_cores']}")
    print(f"RAM total:           {info['ram_total_gb']} GiB")
    print(f"RAM available:       {info['ram_available_gb']} GiB")
    print(f"RAM usage:           {info['ram_usage_percent']}%")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Show basic system information useful for IT support."
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Print the collected information as JSON",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    info = collect_system_info()

    if args.json:
        print(json.dumps(info, indent=2))
    else:
        print_human_readable(info)


if __name__ == "__main__":
    main()
