# 1. Basics

# 1a. Easy commands
| No | Command | Requires `sudo` | Operation |
|:----:|:----|:----|:----|
| 1 | `nmap -sL <networks>` | No | Lists all the targets in the provided networks list and performs reverse DNS lookup. |
| 2 | `nmap -sn <networks>` | No | Discovers live hosts without port scanning (with the **default ping scan**).<br>For root, ARP on local subnet + ICMP echo, ICMP time, TCP SYN to 443.<br>For non-root: TCP connect probes. |

# 1b. Various options
| No | Option | Impact |
|:----:|:----|:----|
| 1  | `-n` | No DNS lookup (default = DNS lookup) |
| 2  | `-R` | Reverse DNS lookup for **all** hosts (online + offline) |
| 3  | `-p-` | Scan **all** ports - equivalent to `-p1-65535` |
| 4  | `-F` | Scan the **100 most common** ports (default = 1000) |
| 5  | `--top-ports 10` | Scan **the 10 most common** ports (default = 1000) |
| 6  | `-r` | Scan ports in consecutive order |
| 7  | `-T0` | Scan speed/timing - Paranoid: super slow, as it scans a port per 5 minutes |
| 8  | `-T1` | Scan speed/timing - Slow: to avoid IDS alerts  |
| 9  | `-T2` | Scan speed/timing - Polite |
| 10 | `-T3` | Scan speed/timing - Normal: the default timing |
| 11 | `-T4` | Scan speed/timing - Aggressive: for learning how to scan targets or in Capture The Flag scenarios |
| 12 | `-T5` | Scan speed/timing - Insane: super quick |
| 13 | `--min-rate 10` | Rate >= 10 packet per second |
| 14 | `--max-rate 10` | Rate <= 10 packet per second |
| 15 | `--min-parallelism 50` | Parallel probes >= 50 |
| 16 | `--max-parallelism 50` | Parallel probes <= 50 |
| 17 | `-f` | IP data fragmentation into 8 Bytes |
| 18 | `-ff` | IP data fragmentation into 16 Bytes |
| 19 | `--reason` | Explanation about how Nmap reached to a conclusion |
| 20 | `-v` | Verbosity Level: Verbose |
| 21 | `-vv` | Verbosity Level: Very Verbose |
| 22 | `-d` | Debugging Level: Debugging |
| 23 | `-dd` | Debugging Level: Details on Debugging |
| 24 | `--source-port <port_number>` | Specify the source port number, otherwise it is random |
| 25 | `--data-length <length>` | Append random non-sense data, just to reach the specified packet length |
| 26 | `-S <spoofed_IP>` | Spoofed IP address |
| 27 | `--spoof-mac <spoofed_MAC>` | Spoofed MAC address |
| 28 | `-D <decoys1>,ME,<decoys2>` | Decoy IPs alongside my IP |
| 29 | `--version-intensity <0-9>` | Determine the level of version intensity checks |
| 30 | `--version-light` | Version intensity level is 2: Try the most likely probes |
| 31 | `--version-all` | Version intensity level is 9: Try all available probes |
| 32 | `--script=<scripts>` | Run the specified NSE scripts under `/usr/share/nmap/scripts` |

# 2. Scan commands

## 2a. Live Host Discovery Scans

| No | Command | Requires `sudo` | Operation |
|:----:|:----|:----|:----|
| 1 | `nmap -PR -sn <targets>` | Yes | ARP scan (**ARP scan for the same subnet**) |
| 2 | `nmap -PE -sn <targets>` | Yes | ICMP Echo scan |
| 3 | `nmap -PP -sn <targets>` | Yes | ICMP Timestamp scan |
| 4 | `nmap -PM -sn <targets>` | Yes | ICMP Address Mask scan |
| 5 | `nmap -PS -sn <targets>` | Yes | TCP SYN ping scan |
| 6 | `nmap -PA -sn <targets>` | Yes | TCP ACK ping scan |
| 7 | `nmap -PU -sn <targets>` | Yes | UDP ping scan |

## 2b. Port Scans

| No | Command | Requires `sudo` | Category | Operation |
|:----:|:----|:----|:----|:----|
| 1  | `nmap -sT <target>` | No | Basic | ~~ TCP Connect Scan ~~<br>Leaves logs, as it completes the 3-way handshake.<br>`SYN --> SYN,ACK --> ACK + RST,ACK` |
| 2  | `nmap -sS <target>` | Yes | Basic | ~~ TCP SYN Scan ~~<br>Stealth scan, as it does **NOT** establish a TCP connection, the handshake is never completed.<br>`SYN --> SYN,ACK --> RST` |
| 3  | `nmap -sU <target>` | Yes | Basic | ~~ UDP Scan ~~<br>UDP does **NOT** require a handshake at all. If a port is *closed*, we expect:<br>`UDP_pkt --> ICMP_type3_code3` |
| 4  | `nmap -sN <target>` | Yes | Advanced | ~~ TCP Null Scan ~~<br>All 6 flags are set to 0. For BSD systems (not Windows, not firewall, not modern Linux), if a port is *closed*, we expect:<br>`TCP_null --> RST,ACK` |
| 5  | `nmap -sF <target>` | Yes | Advanced | ~~ TCP FIN Scan ~~<br>One flag `FIN` is set to 1. For BSD systems (not Windows, not firewall, not modern Linux), if a port is *closed*, we expect:<br>`TCP_FIN --> RST,ACK` |
| 6  | `nmap -sX <target>` | Yes | Advanced | ~~ TCP Xmas Scan ~~<br>Three flags `URG`, `PSH` and `FIN` are set to 1. For BSD systems (not Windows, not firewall, not modern Linux), if a port is *closed*, we expect:<br>`TCP_URG_PSH_FIN --> RST,ACK` |
| 7  | `nmap -sM <target>` | Yes | Advanced | ~~ TCP Maimon Scan ~~<br>Two flags `ACK` and `FIN` are set to 1. **Rather useless scan**. If a port is *closed or open*, we expect:<br>`TCP_ACK_FIN --> RST` |
| 8  | `nmap -sA <target>` | Yes | Advanced | ~~ TCP ACK Scan ~~<br>One flag `ACK` is set to 1. **This scan exposes the firewall rules, NOT the services**. If a port is *closed or open*, we expect:<br>`TCP_ACK --> RST`.<br>If a port is filtered:<br>`No response` / `ICMP unreachable` |
| 9  | `nmap -sW <target>` | Yes | Advanced | ~~ Similar to TCP ACK scan ~~<br>But the `Window` field of `RST` packet is examined. **This scan exposes the firewall rules, NOT the services**. If a port is *closed or open*, we expect:<br>`TCP_ACK --> RST`.<br>If a port is filtered:<br>`No response` / `ICMP unreachable` |
| 10 | `nmap --scanflags URGACKPSHRSTSYNFIN <target>` | Yes | Advanced | ~~ Custom Scan ~~<br>We can set whichever ports we want to 1, but we need to know how the *different ports behave*, in order to interpret the results correctly. |

## 2c. Hiding-identity scans

| No | Command | Requires `sudo` | Reason and impact |
|:----:|:----|:----|:----|
| 1 | `nmap -S <spoofed_IP> <target>` | Yes | Spoofing my IP address requires `sudo`. But the target will **respond to the spoofed IP address**. The attackers must **monitor the network of the spoofed_IP machine** in order to infer things for the target. |
| 2 | `nmap -D <decoys1>,ME,<decoys2> <target>` | No | Make the scan appear as if it is coming from many IP addresses. Our IP will be **blended among a variety of IPs** and we will receive the reply from the target. |
| 3 | `nmap -sI <zombie_IP> <target>` | Yes | ~~ Zombie or idle scan ~~<br>An idle system is prerequisite.<br>1) We trigger the zombie in order to notice its IP ID.<br>2) We send a packet as if it is coming from the zombie machine.<br>3) We trigger again the zombie to notice the new IP ID.<br>-->If the IP IDs differ by 1, the port was *closed or filtered*. If the difference is 2, the port is actually *open*.|

## 2d. Post port scans

| No | Command | Requires `sudo` | Reason and impact |
|:----:|:----|:----|:----|
| 1 | `nmap -sV` | No | Find out the services versions. Running services may be a guess, but services names are **never** a random guess. The scanner actually connects to the port in order to grab the banner. So, stelath scan `-sS` is **never possible** when we choose the option `-sV`, since it needs an established connection. But in term of errors, nmap will not have any problem if one combines them. |
| 2 | `nmap -sS -O` | Yes | Detect the running OS. It is often not accurate. |
| 3 | `nmap --traceroute` | No | Like the common `tracert` command, but with the difference that in Nmap, traceroute begins with the high `TTL` and it keeps decreasing.|
| 4 | `nmap -sC` | Not always | Run the default scripts. Equivalent to: `nmap --script=default`|
| 5 | `nmap -A` | Not always | Equivalent to: `nmap -sV -O -sC --traceroute`|
