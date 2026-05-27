import subprocess
import sys
import ipaddress
import re
import shutil


def check_nmap():
    """Verify nmap is installed."""
    if not shutil.which("nmap"):
        print("[!] Error: nmap is not installed or not in PATH")
        sys.exit(1)


def validate_target(target):
    """Validate the user input is a valid IP, range, or CIDR."""
    target = target.strip()
    # Try CIDR notation
    try:
        ipaddress.ip_network(target, strict=False)
        return target, "cidr"
    except ValueError:
        pass
    # Try single IP
    try:
        ipaddress.ip_address(target)
        return target, "single"
    except ValueError:
        pass
    # Try hyphenated range like 10.0.0.1-50
    if re.match(r"^\d+\.\d+\.\d+\.\d+-\d+$", target):
        return target, "range"
    return None, None


def is_local_subnet(target):
    """Check if the target CIDR is on a directly connected interface."""
    try:
        result = subprocess.run(
            ["ip", "-o", "-4", "addr", "show"],
            capture_output=True, text=True, check=True
        )
        local_nets = []
        for line in result.stdout.splitlines():
            m = re.search(r"inet (\S+)", line)
            if m:
                local_nets.append(ipaddress.ip_network(m.group(1), strict=False))

        target_net = ipaddress.ip_network(target, strict=False)
        for net in local_nets:
            if target_net.subnet_of(net) or net.subnet_of(target_net) or target_net.overlaps(net):
                return True
    except Exception:
        pass
    return False


def run_nmap_scan(target, extra_args=None):
    """Run nmap -sn and return raw output."""
    cmd = ["nmap", "-sn", "-n"]  # -n = no DNS resolution (faster)
    if extra_args:
        cmd.extend(extra_args)
    cmd.append(target)

    print(f"\n[*] Running: {' '.join(cmd)}\n")
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, check=False)
        return result.stdout
    except Exception as e:
        print(f"[!] Error running nmap: {e}")
        sys.exit(1)


def parse_nmap_output(output):
    """
    Parse nmap -sn output. A host is genuinely 'up' only if nmap
    reports 'Host is up' for it. Hosts not reported = down.
    """
    up_hosts = []
    # nmap report blocks: "Nmap scan report for X" followed by "Host is up"
    blocks = re.split(r"Nmap scan report for ", output)
    for block in blocks[1:]:
        # First token is the IP/hostname
        first_line = block.splitlines()[0].strip()
        # Extract IP — handles "hostname (1.2.3.4)" and bare IPs
        ip_match = re.search(r"(\d+\.\d+\.\d+\.\d+)", first_line)
        if not ip_match:
            continue
        ip = ip_match.group(1)
        if "Host is up" in block:
            up_hosts.append(ip)
    return up_hosts


def expand_target(target, target_type):
    """Expand target into a list of all IPs in scope."""
    if target_type == "single":
        return [target]
    if target_type == "cidr":
        net = ipaddress.ip_network(target, strict=False)
        # For /31 and /32, include all; otherwise skip network & broadcast for IPv4
        if net.num_addresses <= 2:
            return [str(h) for h in net]
        return [str(h) for h in net.hosts()]
    if target_type == "range":
        # 10.0.0.1-50
        base, end = target.rsplit(".", 1)[0], target.split("-")[1]
        start = int(target.split(".")[-1].split("-")[0])
        return [f"{base}.{i}" for i in range(start, int(end) + 1)]
    return []


def print_results(all_ips, up_hosts):
    """Pretty print up/down status for every IP in scope."""
    up_set = set(up_hosts)
    print("=" * 50)
    print(f"  Host Discovery Results")
    print("=" * 50)
    for ip in all_ips:
        if ip in up_set:
            # print(f"  \033[92m[+]\033[clear0m {ip:<18} Host is up")
            print(f"[+] {ip:<18} Host is up")
        else:
            # print(f"  \033[91m[-]\033[0m {ip:<18} Host is down")
            print(f"[-] {ip:<18} Host is down")
    print("=" * 50)
    print(f"  Total: {len(all_ips)} | Up: {len(up_hosts)} | Down: {len(all_ips) - len(up_hosts)}")
    print("=" * 50)


def main():
    check_nmap()

    print("=" * 50)
    print("  Nmap Host Discovery (-sn)")
    print("=" * 50)
    target_input = input("[?] Enter target (IP, CIDR, or range): ").strip()

    target, target_type = validate_target(target_input)
    if not target:
        print("[!] Invalid target format.")
        sys.exit(1)

    # Decide on discovery method
    extra_args = []
    if target_type == "cidr" and is_local_subnet(target):
        print("[*] Target appears to be on a local subnet — ARP discovery will be used (reliable).")
    else:
        print("[*] Target is remote — using ICMP echo only (-PE) to avoid false positives.")
        print("    Note: hosts blocking ICMP will appear down. Use -PS/-PA for TCP probes if needed.")
        extra_args = ["-PE"]

    output = run_nmap_scan(target, extra_args)
    up_hosts = parse_nmap_output(output)
    all_ips = expand_target(target, target_type)

    print_results(all_ips, up_hosts)

    # Return the list for chaining into -p- scans
    if up_hosts:
        print("\n[*] Live hosts ready for follow-up scanning:")
        print(",".join(up_hosts))


if __name__ == "__main__":
    main()
