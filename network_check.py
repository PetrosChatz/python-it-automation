#!/usr/bin/env python3
"""Run simple DNS, TCP and ping connectivity checks."""

from __future__ import annotations

import argparse
import platform
import socket
import subprocess


def resolve_host(host: str) -> str | None:
    """Resolve a hostname to an IPv4 address."""
    try:
        return socket.gethostbyname(host)
    except socket.gaierror:
        return None


def tcp_check(host: str, port: int, timeout: float) -> tuple[bool, str]:
    """Attempt a TCP connection to a host and port."""
    try:
        with socket.create_connection((host, port), timeout=timeout):
            return True, f"TCP connection to {host}:{port} succeeded"
    except OSError as exc:
        return False, f"TCP connection to {host}:{port} failed: {exc}"


def ping_host(host: str, timeout: int) -> tuple[bool, str]:
    """Ping a host using the operating system's ping command."""
    system = platform.system().lower()

    if system == "windows":
        command = ["ping", "-n", "1", "-w", str(timeout * 1000), host]
    else:
        command = ["ping", "-c", "1", "-W", str(timeout), host]

    try:
        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
            timeout=timeout + 2,
            check=False,
        )
    except (FileNotFoundError, subprocess.TimeoutExpired) as exc:
        return False, f"Ping could not be completed: {exc}"

    if result.returncode == 0:
        return True, f"Ping to {host} succeeded"
    return False, f"Ping to {host} failed"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Check DNS resolution, TCP connectivity and ICMP reachability."
    )
    parser.add_argument("host", nargs="?", default="example.com", help="Host to test")
    parser.add_argument("--port", type=int, default=443, help="TCP port (default: 443)")
    parser.add_argument(
        "--timeout", type=int, default=3, help="Timeout in seconds (default: 3)"
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()

    print("NETWORK CONNECTIVITY CHECK")
    print("=" * 26)
    print(f"Target: {args.host}:{args.port}\n")

    ip = resolve_host(args.host)
    if ip:
        print(f"[OK] DNS resolution: {args.host} -> {ip}")
    else:
        print(f"[FAIL] DNS resolution failed for {args.host}")

    tcp_ok, tcp_message = tcp_check(args.host, args.port, args.timeout)
    print(f"[{'OK' if tcp_ok else 'FAIL'}] {tcp_message}")

    ping_ok, ping_message = ping_host(args.host, args.timeout)
    print(f"[{'OK' if ping_ok else 'FAIL'}] {ping_message}")

    print("\nNote: a failed ping does not always mean the host is offline; ICMP may be blocked.")


if __name__ == "__main__":
    main()
