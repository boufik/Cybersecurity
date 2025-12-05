# 1. Basic Commands

| No | Command | Requires `sudo` | Operation |
|:----:|:----|:----|:----|
| 1 | `nmap -sL <networks>` | No | List all the losts in the provided networks list |
| 2 | `nmap -sn <networks>` | No | Discover live hosts without port scanning (with the **default ping scan**) |

# 2. Live Host Discovery

## 2a. Basic scans

| No | Command | Requires `sudo` | Operation |
|:----:|:----|:----|:----|
| 1 | `nmap -PR -sn <targets>` | Yes | ARP scan (**ARP scan for the same subnet**) |
| 2 | `nmap -PE -sn <targets>` | Yes | ICMP Echo scan (**ARP scan for the same subnet**) |
| 3 | `nmap -PP -sn <targets>` | Yes | ICMP Timestamp scan (**ARP scan for the same subnet**) |
| 4 | `nmap -PM -sn <targets>` | Yes | ICMP Address Mask scan (**ARP scan for the same subnet**) |
| 5 | `nmap -PS -sn <targets>` | Yes | TCP SYN ping scan (**ARP scan for the same subnet**) |
| 6 | `nmap -PA -sn <targets>` | Yes | TCP ACK ping scan (**ARP scan for the same subnet**) |
| 7 | `nmap -PU -sn <targets>` | Yes | UDP ping scan (**ARP scan for the same subnet**) |

## 2b. Advanced scans
