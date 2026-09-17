#!/usr/bin/env python3
"""Check disk usage and warn when a configurable threshold is exceeded."""

from __future__ import annotations

import argparse
import shutil
from pathlib import Path


def bytes_to_gb(value: int) -> float:
    return round(value / (1024**3), 2)


def get_disk_usage(path: Path) -> dict[str, float]:
    """Return disk usage values for the filesystem containing path."""
    total, used, free = shutil.disk_usage(path)
    percent_used = (used / total * 100) if total else 0.0

    return {
        "total_gb": bytes_to_gb(total),
        "used_gb": bytes_to_gb(used),
        "free_gb": bytes_to_gb(free),
        "percent_used": round(percent_used, 2),
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Monitor local disk usage.")
    parser.add_argument(
        "path",
        nargs="?",
        type=Path,
        default=Path.cwd(),
        help="Path on the filesystem to inspect (default: current directory)",
    )
    parser.add_argument(
        "--threshold",
        type=float,
        default=80.0,
        help="Warning threshold as percentage used (default: 80)",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()

    if not args.path.exists():
        raise SystemExit(f"Path does not exist: {args.path}")

    if not 0 <= args.threshold <= 100:
        raise SystemExit("Threshold must be between 0 and 100")

    usage = get_disk_usage(args.path)

    print("DISK USAGE MONITOR")
    print("=" * 18)
    print(f"Path:       {args.path.resolve()}")
    print(f"Total:      {usage['total_gb']} GiB")
    print(f"Used:       {usage['used_gb']} GiB")
    print(f"Free:       {usage['free_gb']} GiB")
    print(f"Usage:      {usage['percent_used']}%")
    print(f"Threshold:  {args.threshold}%")

    if usage["percent_used"] >= args.threshold:
        print("\n[WARNING] Disk usage is at or above the configured threshold.")
    else:
        print("\n[OK] Disk usage is below the configured threshold.")


if __name__ == "__main__":
    main()
