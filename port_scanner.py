#!/usr/bin/env python3
"""Port scanner with service banner grabbing."""

import socket
import concurrent.futures
from datetime import datetime

TIMEOUT = 1.0
MAX_WORKERS = 100
PORT_RANGE = (1, 1024)

COMMON_PORTS: dict[int, str] = {
    21: "FTP", 22: "SSH", 23: "Telnet", 25: "SMTP", 53: "DNS",
    80: "HTTP", 110: "POP3", 143: "IMAP", 443: "HTTPS", 445: "SMB",
    3306: "MySQL", 3389: "RDP", 5432: "PostgreSQL", 6379: "Redis",
    8080: "HTTP-Alt", 8443: "HTTPS-Alt", 27017: "MongoDB",
}


def grab_banner(ip: str, port: int) -> str | None:
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(TIMEOUT)
            s.connect((ip, port))
            # Send a generic probe; many services respond unprompted
            try:
                s.sendall(b"HEAD / HTTP/1.0\r\n\r\n")
            except OSError:
                pass
            banner = s.recv(1024).decode(errors="replace").strip()
            return banner[:200] if banner else None
    except (OSError, socket.timeout):
        return None


def scan_port(ip: str, port: int) -> tuple[int, bool, str | None]:
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(TIMEOUT)
            open_ = s.connect_ex((ip, port)) == 0
    except OSError:
        open_ = False

    if not open_:
        return port, False, None

    banner = grab_banner(ip, port)
    return port, True, banner


def identify_service(port: int, banner: str | None) -> str:
    known = COMMON_PORTS.get(port)
    if known:
        return known

    if banner:
        low = banner.lower()
        if "ssh" in low:
            return "SSH"
        if "ftp" in low:
            return "FTP"
        if "smtp" in low or "220" in low:
            return "SMTP"
        if "http" in low or "html" in low:
            return "HTTP"
        if "mysql" in low:
            return "MySQL"
        if "postgresql" in low or "postgres" in low:
            return "PostgreSQL"
        if "redis" in low:
            return "Redis"
        if "mongodb" in low:
            return "MongoDB"

    return "Unknown"


def resolve_host(target: str) -> str:
    try:
        return socket.gethostbyname(target)
    except socket.gaierror as exc:
        raise SystemExit(f"[!] Cannot resolve host '{target}': {exc}") from exc


def scan(target: str, start: int = PORT_RANGE[0], end: int = PORT_RANGE[1]) -> None:
    ip = resolve_host(target)
    total = end - start + 1

    print(f"\n{'='*60}")
    print(f"  Target : {target} ({ip})")
    print(f"  Ports  : {start}-{end}  ({total} ports)")
    print(f"  Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"{'='*60}\n")

    open_ports: list[tuple[int, str | None, str]] = []

    with concurrent.futures.ThreadPoolExecutor(max_workers=MAX_WORKERS) as pool:
        futures = {pool.submit(scan_port, ip, p): p for p in range(start, end + 1)}
        done = 0
        for future in concurrent.futures.as_completed(futures):
            done += 1
            print(f"\r  Scanning... {done}/{total}", end="", flush=True)
            port, is_open, banner = future.result()
            if is_open:
                service = identify_service(port, banner)
                open_ports.append((port, banner, service))

    print(f"\r  Scanning... done{' '*20}\n")

    if not open_ports:
        print("  No open ports found.\n")
        return

    open_ports.sort(key=lambda x: x[0])
    print(f"  {'PORT':<8} {'SERVICE':<16} {'BANNER'}")
    print(f"  {'-'*7} {'-'*15} {'-'*35}")
    for port, banner, service in open_ports:
        banner_preview = (banner[:50] + "...") if banner and len(banner) > 50 else (banner or "")
        print(f"  {port:<8} {service:<16} {banner_preview}")

    print(f"\n  {len(open_ports)} open port(s) found.")
    print(f"  Finished: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")


if __name__ == "__main__":
    target_input = input("Enter target IP or hostname: ").strip()
    custom = input("Custom port range? (y/N): ").strip().lower()

    if custom == "y":
        start_port = int(input("  Start port: ").strip())
        end_port = int(input("  End port  : ").strip())
    else:
        start_port, end_port = PORT_RANGE

    scan(target_input, start_port, end_port)
