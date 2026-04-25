import subprocess
import sys


def ping(host: str, count: int = 1, timeout: int = 1) -> bool:
    cmd = ["ping", "-c", str(count), "-W", str(timeout), host]
    return subprocess.run(cmd, capture_output=True, text=True).returncode == 0


def ping_ips(network: str) -> list[str]:
    open_hosts = []
    for i in range(1, 255):  # .1–.254 (skip network/broadcast addresses)
        host = f"{network}{i}"
        status = ping(host)
        print(f"{host}: {'Open' if status else 'Closed'}")
        if status:
            open_hosts.append(host)
    return open_hosts


def parse_network_base(network: str) -> str:
    """Return the base prefix (e.g. '192.168.1.') from any of:
    '192.168.1', '192.168.1.0', '192.168.1.100'
    """
    octets = network.strip().split(".")
    base_octets = [o for o in octets if o][:3]
    if len(base_octets) != 3:
        raise ValueError(f"Expected at least 3 octets, got: {network!r}")
    if not all(o.isdigit() and 0 <= int(o) <= 255 for o in base_octets):
        raise ValueError(f"Invalid IP octets in: {network!r}")
    return ".".join(base_octets) + "."


def run() -> None:
    network = input("Network IP (e.g. 192.168.1): ").strip()
    try:
        network_base = parse_network_base(network)
    except ValueError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

    open_hosts = ping_ips(network_base)
    print(f"\nOpen hosts ({len(open_hosts)}): {open_hosts}")


if __name__ == "__main__":
    run()
