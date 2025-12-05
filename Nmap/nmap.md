# 1. Basics

# 1a. Easy commands
| No | Command | Requires `sudo` | Operation |
|:----:|:----|:----|:----|
| 1 | `nmap -sL <networks>` | No | List all the losts in the provided networks list |
| 2 | `nmap -sn <networks>` | No | Discover live hosts without port scanning (with the **default ping scan**) |

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
| 19 | `--reason` | Verbosity Level: Explanation about how Nmap reached to a conclusion |
| 20 | `-v` | Verbosity Level: Verbose |
| 21 | `-vv` | Verbosity Level: Very Verbose |
| 22 | `-d` | Verbosity Level: Debugging |
| 23 | `-dd` | Verbosity Level: Details on Debugging |
| 24 | `--source-port <port_number>` | Specify the source port number, otherwise it is random |
| 25 | `--data-length <length>` | Append random non-sense data, just to reach the specified packet length |

# 2. Scan commands

## 2a. Live Host Discovery Scans

| No | Command | Requires `sudo` | Operation |
|:----:|:----|:----|:----|
| 1 | `nmap -PR -sn <targets>` | Yes | ARP scan (**ARP scan for the same subnet**) |
| 2 | `nmap -PE -sn <targets>` | Yes | ICMP Echo scan (**ARP scan for the same subnet**) |
| 3 | `nmap -PP -sn <targets>` | Yes | ICMP Timestamp scan (**ARP scan for the same subnet**) |
| 4 | `nmap -PM -sn <targets>` | Yes | ICMP Address Mask scan (**ARP scan for the same subnet**) |
| 5 | `nmap -PS -sn <targets>` | Yes | TCP SYN ping scan (**ARP scan for the same subnet**) |
| 6 | `nmap -PA -sn <targets>` | Yes | TCP ACK ping scan (**ARP scan for the same subnet**) |
| 7 | `nmap -PU -sn <targets>` | Yes | UDP ping scan (**ARP scan for the same subnet**) |

## 2b. Port Scans

| No | Command | Requires `sudo` | Category | Operation |
|:----:|:----|:----|:----|:----|
| 1  | `nmap -sT <target>` | No | Basic | TCP Connect Scan: Leaves logs, as it completes the 3-way handshake<br>`SYN -> SYN,ACK -> ACK + RST,ACK` |
| 2  | `nmap -sS <target>` | Yes | Basic | TCP SYN Scan: Stealth scan, as it does **NOT** establish a TCP connection, the handshake is never completed<br>`SYN -> SYN,ACK -> RST` |
| 3  | `nmap -sU <target>` | Yes | Basic | UDP Scan: UDP does **NOT** require a handshake at all. If a port is closed, then we have this sequence:<br>`UDP_pkt -> ICMP_type3_code3` |
