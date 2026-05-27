#!/usr/bin/env python3
"""
Host discovery with false-positive filtering.
Handles the /24 'all hosts up' issue by filtering on latency
and verifying with TCP probes.
"""

import subprocess
import sys
import ipaddress
import re
import shutil
import socket
from concurrent.futures import ThreadPoolExecutor


# ANSI colors
GREEN = "\033[92m"
RED = "\033[91m"
YELLOW = "\033[93m"
CYAN = "\033[96m"
RESET = "\033[0m"


def check_nmap():
    if not shutil.which("nmap"):
        print(f"{RED}[!] nmap not found in PATH{RESET}")
        sys.exit(1)


def validate_target(target):
    target = target.strip()
    try:
        ipaddress.ip_network(target, strict=False)
        return target, "cidr"
    except ValueError:
        pass
    try:
        ipaddress.ip_address(target)
        return target, "single"
    except ValueError:
        pass
    if re.match(r"^\d+\.\d+\.\d+\.\d+-\d+$", target):
        return target, "range"
    return None, None


def expand_target(target, target_type):
    if target_type == "single":
        return [target]
    if target_type == "cidr":
        net = ipaddress.ip_network(target, strict=False)
        if net.num_addresses <= 2:
            return [str(h) for h in net]
        return [str(h) for h in net.hosts()]
    if target_type == "range":
        base = target.rsplit(".", 1)[0]
        start = int(target.split(".")[-1].split("-")[0])
        end = int(target.split("-")[1])
        return [f"{base}.{i}" for i in range(start, end + 1)]
    return []


def run_nmap_scan(target):
    cmd = ["nmap", "-sn", "-n", "-PE", target]
    print(f"\n{CYAN}[*] Running: {' '.join(cmd)}{RESET}\n")
    result = subprocess.run(cmd, capture_output=True, text=True, check=False)
    return result.stdout


def parse_nmap_output(output):
    """Return list of (ip, latency_seconds) tuples for hosts reported up."""
    up_hosts = []
    blocks = re.split(r"Nmap scan report for ", output)
    for block in blocks[1:]:
        first_line = block.splitlines()[0].strip()
        ip_match = re.search(r"(\d+\.\d+\.\d+\.\d+)", first_line)
        if not ip_match:
            continue
        if "Host is up" not in block:
            continue
        ip = ip_match.group(1)
        lat_match = re.search(r"Host is up \(([\d.]+)s latency\)", block)
        latency = float(lat_match.group(1)) if lat_match else 0.0
        up_hosts.append((ip, latency))
    return up_hosts


def tcp_verify(ip, ports=(80, 443, 22, 445, 139, 3389, 8080, 53), timeout=1.0):
    """
    Return True if any TCP probe shows the host's stack is alive.
    Open ports AND 'connection refused' both confirm a real host.
    Only timeouts on all ports = probably a ghost.
    """
    for port in ports:
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.settimeout(timeout)
                result = s.connect_ex((ip, port))
                if result == 0:
                    return True  # port open
                if result in (111, 61, 10061):  # ECONNREFUSED on Linux/BSD/Win
                    return True  # host's TCP stack replied
        except (socket.timeout, OSError):
            continue
    return False


def verify_hosts_parallel(hosts, max_workers=50):
    print(f"{CYAN}[*] Verifying {len(hosts)} suspect hosts with TCP probes...{RESET}")
    with ThreadPoolExecutor(max_workers=max_workers) as ex:
        results = list(ex.map(tcp_verify, hosts))
    return [ip for ip, alive in zip(hosts, results) if alive]


def print_results(all_ips, confirmed_up):
    up_set = set(confirmed_up)
    print(f"\n{'=' * 55}")
    print(f"  Host Discovery Results")
    print(f"{'=' * 55}")
    for ip in all_ips:
        if ip in up_set:
            print(f"  {GREEN}[+]{RESET} {ip:<18} Host is up")
        else:
            print(f"  {RED}[-]{RESET} {ip:<18} Host is down")
    print(f"{'=' * 55}")
    print(f"  Total: {len(all_ips)} | Up: {len(confirmed_up)} | "
          f"Down: {len(all_ips) - len(confirmed_up)}")
    print(f"{'=' * 55}")


def main():
    check_nmap()

    print(f"{'=' * 55}")
    print(f"  Nmap Host Discovery with FP Filtering")
    print(f"{'=' * 55}")
    target_input = input(f"{CYAN}[?] Target (IP / CIDR / range): {RESET}").strip()

    target, target_type = validate_target(target_input)
    if not target:
        print(f"{RED}[!] Invalid target.{RESET}")
        sys.exit(1)

    # Step 1: nmap -sn
    output = run_nmap_scan(target)
    raw_up = parse_nmap_output(output)
    print(f"{YELLOW}[*] nmap reported {len(raw_up)} hosts up (pre-filter){RESET}")

    # Step 2: latency filter — anything over 50ms on local net is suspect
    LATENCY_THRESHOLD = 0.05
    trusted = [ip for ip, lat in raw_up if lat <= LATENCY_THRESHOLD]
    suspect = [ip for ip, lat in raw_up if lat > LATENCY_THRESHOLD]
    print(f"{CYAN}[*] {len(trusted)} hosts trusted (latency <= {LATENCY_THRESHOLD*1000:.0f}ms){RESET}")
    print(f"{YELLOW}[*] {len(suspect)} hosts suspect (high latency — verifying){RESET}")

    # Step 3: TCP-verify the suspects
    verified_suspects = verify_hosts_parallel(suspect) if suspect else []
    if suspect:
        print(f"{CYAN}[*] {len(verified_suspects)} suspects passed TCP verification{RESET}")

    confirmed_up = sorted(set(trusted) | set(verified_suspects),
                          key=lambda x: tuple(int(o) for o in x.split(".")))

    all_ips = expand_target(target, target_type)
    print_results(all_ips, confirmed_up)

    if confirmed_up:
        print(f"\n{GREEN}[*] Confirmed live hosts (safe for -p- follow-up):{RESET}")
        print(",".join(confirmed_up))


if __name__ == "__main__":
    main()