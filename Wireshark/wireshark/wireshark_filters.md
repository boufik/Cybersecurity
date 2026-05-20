# Wireshark Display Filters — Cheat Sheet

> A reference of display filters organized by protocol/category. Covers everyday troubleshooting plus reconnaissance-oriented filters. All examples use Wireshark's `protocol.field` syntax with `==`, `!=`, `contains`, `matches`, `and`, `or`, `not`.

---

## Table of Contents

1. [Operators and Syntax Quick Reference](#1-operators-and-syntax-quick-reference)
2. [Ethernet and MAC Layer](#2-ethernet-and-mac-layer)
3. [ARP](#3-arp)
4. [IPv4 / IPv6](#4-ipv4--ipv6)
5. [ICMP / ICMPv6](#5-icmp--icmpv6)
6. [TCP](#6-tcp)
7. [UDP](#7-udp)
8. [DNS](#8-dns)
9. [DHCP / DHCPv6](#9-dhcp--dhcpv6)
10. [HTTP](#10-http)
11. [TLS / SSL](#11-tls--ssl)
12. [SSH](#12-ssh)
13. [FTP](#13-ftp)
14. [SMTP / POP3 / IMAP](#14-smtp--pop3--imap)
15. [SMB / NetBIOS](#15-smb--netbios)
16. [LDAP / Kerberos](#16-ldap--kerberos)
17. [SNMP](#17-snmp)
18. [mDNS / LLMNR / SSDP](#18-mdns--llmnr--ssdp)
19. [VLAN / Tunneling](#19-vlan--tunneling)
20. [Wireless (802.11)](#20-wireless-80211)
21. [Recon-Specific Combined Filters](#21-recon-specific-combined-filters)
22. [Troubleshooting / Anomaly Filters](#22-troubleshooting--anomaly-filters)

---

## 1. Operators and Syntax Quick Reference

| Filter | Purpose |
|---|---|
| `==` or `eq` | Equals |
| `!=` or `ne` | Not equals |
| `>` `<` `>=` `<=` | Numeric comparisons (also `gt`, `lt`, `ge`, `le`) |
| `&&` or `and` | Logical AND |
| `\|\|` or `or` | Logical OR |
| `!` or `not` | Logical NOT |
| `contains` | Substring match in a field |
| `matches` | Regex match (Perl-compatible) |
| `in` | Membership test, e.g. `tcp.port in {80 443 8080}` |
| `field` (alone) | True if the field exists in the packet |
| `!field` | True if the field is absent |

---

## 2. Ethernet and MAC Layer

| Filter | Purpose |
|---|---|
| `eth.addr == aa:bb:cc:dd:ee:ff` | Source MAC or destination MAC |
| `eth.src == aa:bb:cc:dd:ee:ff` | Source MAC only |
| `eth.dst == aa:bb:cc:dd:ee:ff` | Destination MAC only |
| `eth.type == 0x0800` | EtherType IPv4 (0x86dd = IPv6, 0x0806 = ARP) |
| `eth.dst == ff:ff:ff:ff:ff:ff` | Broadcast frames |
| `eth.dst[0] & 1` | Any multicast/broadcast frame (group bit set) |
| `eth.addr matches "^00:0c:29"` | Match an OUI prefix (here: VMware) |
| `vlan.id == 10` | Frames tagged VLAN 10 |
| `frame.len > 1500` | Jumbo frames or oversized payloads |
| `frame.time_delta > 1` | Packets with >1s gap from the previous |

---

## 3. ARP

| Filter | Purpose |
|---|---|
| `arp` | All ARP traffic |
| `arp.opcode == 1` | ARP requests ("who has...") |
| `arp.opcode == 2` | ARP replies ("...is at") |
| `arp.src.proto_ipv4 == 192.168.1.1` | ARP packet where this is the sender IP |
| `arp.dst.proto_ipv4 == 192.168.1.1` | ARP packet where this is the target IP |
| `arp.src.hw_mac == aa:bb:cc:dd:ee:ff` | Sender MAC inside the ARP payload |
| `arp.duplicate-address-detected` | Gratuitous ARP / duplicate IP warning |
| `arp.isgratuitous` | Gratuitous ARP announcements |
| `arp and arp.src.proto_ipv4 != arp.dst.proto_ipv4` | Active ARP request/reply (excludes self-announcements) |

---

## 4. IPv4 / IPv6

| Filter | Purpose |
|---|---|
| `ip.addr == 192.168.1.50` | Source OR destination IPv4 |
| `ip.src == 192.168.1.50` | Source IPv4 only |
| `ip.dst == 192.168.1.50` | Destination IPv4 only |
| `ip.addr == 192.168.1.0/24` | Entire subnet (CIDR works) |
| `ip.src in {10.0.0.1 10.0.0.2 10.0.0.3}` | Membership in an IP set |
| `ip.ttl < 10` | Low TTL — possible traceroute or near-expiry packet |
| `ip.ttl == 64` | Typical Linux/macOS default TTL (recon: OS hint) |
| `ip.ttl == 128` | Typical Windows default TTL (recon: OS hint) |
| `ip.flags.df == 1` | "Don't fragment" flag set |
| `ip.flags.mf == 1` | "More fragments" flag — packet is fragmented |
| `ip.frag_offset > 0` | A non-first fragment |
| `ip.len > 1000` | Larger IPv4 packets |
| `ip.proto == 6` | TCP (1=ICMP, 17=UDP, 47=GRE, 50=ESP) |
| `ipv6.addr == fe80::1` | Source OR destination IPv6 |
| `ipv6.src == fe80::1` | Source IPv6 only |
| `ipv6.dst == ff02::1` | Destination IPv6 only |
| `ipv6.addr == 2001:db8::/32` | IPv6 subnet match |
| `ipv6.hlim < 10` | Low hop limit (IPv6 equivalent of TTL) |

---

## 5. ICMP / ICMPv6

| Filter | Purpose |
|---|---|
| `icmp` | All ICMP traffic |
| `icmp.type == 8` | Echo request (ping out) |
| `icmp.type == 0` | Echo reply (ping back) |
| `icmp.type == 3` | Destination unreachable |
| `icmp.type == 3 and icmp.code == 3` | Port unreachable (recon: closed UDP port indicator) |
| `icmp.type == 11` | Time exceeded (traceroute) |
| `icmp.type == 5` | Redirect |
| `icmp.type == 13 or icmp.type == 14` | Timestamp request/reply |
| `icmpv6.type == 128` | IPv6 echo request |
| `icmpv6.type == 129` | IPv6 echo reply |
| `icmpv6.type == 133` | Router solicitation |
| `icmpv6.type == 134` | Router advertisement |
| `icmpv6.type == 135` | Neighbor solicitation (IPv6 ARP equivalent) |
| `icmpv6.type == 136` | Neighbor advertisement |

---

## 6. TCP

| Filter | Purpose |
|---|---|
| `tcp` | All TCP traffic |
| `tcp.port == 443` | Source OR destination port 443 |
| `tcp.srcport == 443` | Source port only |
| `tcp.dstport == 22` | Destination port only |
| `tcp.port in {80 443 8080 8443}` | Multiple ports |
| `tcp.flags.syn == 1 and tcp.flags.ack == 0` | SYN only — connection initiation (recon: scan or new conn) |
| `tcp.flags.syn == 1 and tcp.flags.ack == 1` | SYN-ACK — accepted handshake |
| `tcp.flags.fin == 1` | FIN — graceful close |
| `tcp.flags.reset == 1` | RST — abrupt termination (recon: refused/closed port) |
| `tcp.flags.push == 1` | PSH — push data immediately |
| `tcp.flags == 0x002` | Pure SYN (exact flag value) |
| `tcp.flags == 0x014` | RST+ACK |
| `tcp.window_size == 0` | Zero window — receiver pause/problem indicator |
| `tcp.analysis.retransmission` | Wireshark-detected retransmission |
| `tcp.analysis.duplicate_ack` | Duplicate ACK — packet loss indicator |
| `tcp.analysis.out_of_order` | Out-of-order delivery |
| `tcp.analysis.zero_window` | Zero window event |
| `tcp.analysis.flags` | Any TCP analysis warning |
| `tcp.stream eq 5` | All packets in stream #5 (use Follow → TCP Stream) |
| `tcp.len > 0` | Packets carrying actual TCP payload (excludes pure ACKs) |
| `tcp.options.mss_val < 1460` | Non-default MSS (recon: OS/fingerprint hint) |
| `tcp.payload contains "password"` | Payload substring search |

---

## 7. UDP

| Filter | Purpose |
|---|---|
| `udp` | All UDP traffic |
| `udp.port == 53` | DNS by port |
| `udp.srcport == 67 or udp.srcport == 68` | DHCP ports |
| `udp.port == 123` | NTP |
| `udp.port == 161 or udp.port == 162` | SNMP |
| `udp.port == 500 or udp.port == 4500` | IPsec/IKE |
| `udp.length > 512` | Larger UDP datagrams (recon: possibly amplification candidates) |
| `udp.stream eq 3` | All packets in UDP stream #3 |
| `udp.checksum == 0` | UDP with no checksum (recon/anomaly) |

---

## 8. DNS

| Filter | Purpose |
|---|---|
| `dns` | All DNS traffic |
| `dns.flags.response == 0` | Queries only |
| `dns.flags.response == 1` | Responses only |
| `dns.qry.name == "example.com"` | Exact query name |
| `dns.qry.name contains "google"` | Substring match on query name |
| `dns.qry.name matches "(?i)\\.ru$"` | Regex — domains ending in .ru |
| `dns.qry.type == 1` | A record queries |
| `dns.qry.type == 28` | AAAA record queries |
| `dns.qry.type == 15` | MX record queries (recon: mail infrastructure) |
| `dns.qry.type == 16` | TXT record queries (recon: SPF, DKIM, ownership) |
| `dns.qry.type == 2` | NS record queries (recon: nameservers) |
| `dns.qry.type == 252` | AXFR — zone transfer attempt |
| `dns.flags.rcode == 3` | NXDOMAIN — name does not exist |
| `dns.flags.rcode != 0` | Any DNS error response |
| `dns.a == 8.8.8.8` | Responses containing this A record |
| `dns.resp.name contains "cloudfront"` | Responses for CDN-hosted names |
| `dns.count.answers > 5` | Large answer sets |
| `dns.qry.name.len > 50` | Long query names (recon: tunneling indicator) |

---

## 9. DHCP / DHCPv6

| Filter | Purpose |
|---|---|
| `dhcp` | All DHCP (v4) traffic |
| `dhcp.option.dhcp == 1` | DHCPDISCOVER |
| `dhcp.option.dhcp == 2` | DHCPOFFER |
| `dhcp.option.dhcp == 3` | DHCPREQUEST |
| `dhcp.option.dhcp == 5` | DHCPACK |
| `dhcp.option.dhcp == 6` | DHCPNAK |
| `dhcp.option.dhcp == 7` | DHCPRELEASE |
| `dhcp.hw.mac_addr == aa:bb:cc:dd:ee:ff` | Client MAC inside DHCP |
| `dhcp.option.hostname` | Packets that include a Hostname option (recon: client names) |
| `dhcp.option.hostname contains "android"` | Hostname substring (recon: device fingerprinting) |
| `dhcp.option.requested_ip_address == 192.168.1.50` | Client requesting a specific IP |
| `dhcp.option.vendor_class_id contains "MSFT"` | Vendor class ID (recon: OS/device family) |
| `dhcpv6` | All DHCPv6 traffic |

---

## 10. HTTP

| Filter | Purpose |
|---|---|
| `http` | All HTTP traffic |
| `http.request` | Requests only |
| `http.response` | Responses only |
| `http.request.method == "GET"` | GET requests |
| `http.request.method == "POST"` | POST requests (recon: form submissions, logins) |
| `http.request.method in {"PUT" "DELETE" "PATCH"}` | Write methods |
| `http.host == "example.com"` | Exact Host header |
| `http.host contains "admin"` | Substring on Host (recon: admin panels) |
| `http.request.uri contains "login"` | URI substring (recon: auth endpoints) |
| `http.request.uri matches "\\.(zip\\|tar\\|gz\\|rar)$"` | Downloadable archives |
| `http.user_agent` | Any packet with a User-Agent (recon: client inventory) |
| `http.user_agent contains "curl"` | Specific UA (recon: scripted clients) |
| `http.user_agent contains "Mozilla"` | Browser-style UAs |
| `http.server` | Any packet with a Server header (recon: banner grab) |
| `http.server contains "nginx"` | Server software family |
| `http.response.code == 200` | OK responses |
| `http.response.code == 404` | Not Found |
| `http.response.code >= 500` | Server errors |
| `http.response.code >= 400` | Any client/server error |
| `http.authorization` | Packets with Authorization header (recon: auth in flight) |
| `http.cookie` | Packets with Cookie header |
| `http.content_type contains "json"` | JSON API traffic |
| `http.referer contains "google"` | Referer header substring |
| `http.file_data contains "password"` | Substring inside HTTP body |
| `http2` | HTTP/2 traffic |
| `http2.header.value contains "example.com"` | HTTP/2 header value match |

---

## 11. TLS / SSL

| Filter | Purpose |
|---|---|
| `tls` | All TLS traffic |
| `tls.handshake` | TLS handshake messages only |
| `tls.handshake.type == 1` | Client Hello (recon: outgoing TLS destinations) |
| `tls.handshake.type == 2` | Server Hello |
| `tls.handshake.type == 11` | Certificate message |
| `tls.handshake.type == 14` | Server Hello Done |
| `tls.handshake.type == 16` | Client Key Exchange |
| `tls.handshake.extensions_server_name` | Any packet with SNI (recon: hostname even over HTTPS) |
| `tls.handshake.extensions_server_name == "example.com"` | Specific SNI |
| `tls.handshake.extensions_server_name contains "bank"` | SNI substring |
| `tls.handshake.version == 0x0303` | TLS 1.2 |
| `tls.handshake.version == 0x0304` | TLS 1.3 |
| `tls.handshake.ciphersuites` | Packets advertising cipher suites (recon: client fingerprint / JA3) |
| `tls.handshake.certificate` | Packets containing a server certificate |
| `tls.handshake.ja3_full` | JA3 fingerprint field (if calculated) |
| `tls.alert_message` | TLS alert (errors, close notifies) |
| `tls.record.content_type == 23` | Application data (encrypted payload) |
| `tls.record.version == 0x0301` | SSL 3.1 / TLS 1.0 record version |
| `ssl` | Legacy alias — still works in some versions |

---

## 12. SSH

| Filter | Purpose |
|---|---|
| `ssh` | All SSH traffic |
| `tcp.port == 22` | SSH by default port |
| `ssh.protocol` | Banner exchange packets (recon: version banner) |
| `ssh.message_code == 20` | Key exchange init |
| `ssh.message_code == 21` | New keys |
| `ssh.encrypted_packet` | Encrypted SSH payload after handshake |
| `ssh.protocol contains "OpenSSH"` | OpenSSH banner match (recon: server software) |

---

## 13. FTP

| Filter | Purpose |
|---|---|
| `ftp` | FTP control channel |
| `ftp-data` | FTP data channel |
| `ftp.request.command == "USER"` | Username submission (cleartext) |
| `ftp.request.command == "PASS"` | Password submission (cleartext) |
| `ftp.request.command in {"RETR" "STOR"}` | File downloads/uploads |
| `ftp.response.code == 220` | Service ready banner (recon: server version) |
| `ftp.response.code == 230` | Login successful |
| `ftp.response.code == 530` | Login failed |
| `ftp.response.arg contains "vsFTPd"` | Banner substring (recon) |

---

## 14. SMTP / POP3 / IMAP

| Filter | Purpose |
|---|---|
| `smtp` | All SMTP traffic |
| `smtp.req.command == "MAIL"` | Sender command |
| `smtp.req.command == "RCPT"` | Recipient command |
| `smtp.req.command == "EHLO"` | EHLO greeting (recon: client identification) |
| `smtp.response.code == 220` | Server ready banner |
| `smtp.response.code == 250` | Command OK |
| `smtp.response.code == 535` | Auth failed |
| `smtp.auth.username` | Cleartext username (if not over TLS) |
| `pop` | All POP3 traffic |
| `pop.request.command == "USER"` | POP3 username |
| `pop.request.command == "PASS"` | POP3 password (cleartext) |
| `imap` | All IMAP traffic |
| `imap.request contains "LOGIN"` | IMAP login command |

---

## 15. SMB / NetBIOS

| Filter | Purpose |
|---|---|
| `smb` | SMB v1 |
| `smb2` | SMB v2/v3 |
| `smb2.cmd == 0` | Negotiate (recon: dialect/capability discovery) |
| `smb2.cmd == 1` | Session setup |
| `smb2.cmd == 3` | Tree connect (share access) |
| `smb2.cmd == 5` | Create (open file) |
| `smb2.filename contains "passwd"` | Filename substring |
| `smb2.tree contains "ADMIN$"` | Administrative share access (recon: privileged ops) |
| `smb.server` | SMB server name field |
| `smb.native_os` | Native OS string (recon: OS fingerprint) |
| `smb.native_lanman` | Native LAN Manager string (recon: version) |
| `nbns` | NetBIOS name service |
| `nbns.name contains "WORKGROUP"` | NetBIOS workgroup announcements |
| `browser` | Browser protocol (Windows network neighborhood) |

---

## 16. LDAP / Kerberos

| Filter | Purpose |
|---|---|
| `ldap` | All LDAP traffic |
| `ldap.bindRequest_element` | Bind requests (recon: auth attempts) |
| `ldap.name` | DN field — distinguished names being queried |
| `ldap.filter contains "objectClass=user"` | User enumeration filters |
| `kerberos` | All Kerberos traffic |
| `kerberos.msg_type == 10` | AS-REQ (authentication request) |
| `kerberos.msg_type == 11` | AS-REP |
| `kerberos.msg_type == 12` | TGS-REQ (ticket request) |
| `kerberos.msg_type == 13` | TGS-REP |
| `kerberos.CNameString` | Client principal name (recon: usernames) |
| `kerberos.realm` | Kerberos realm (recon: AD domain name) |

---

## 17. SNMP

| Filter | Purpose |
|---|---|
| `snmp` | All SNMP traffic |
| `snmp.community == "public"` | Default community string (recon: weak config) |
| `snmp.community == "private"` | Write community (recon) |
| `snmp.community` | Any community string field (recon: cleartext creds in v1/v2c) |
| `snmp.version == 0` | SNMPv1 |
| `snmp.version == 1` | SNMPv2c |
| `snmp.version == 3` | SNMPv3 |

---

## 18. mDNS / LLMNR / SSDP

| Filter | Purpose |
|---|---|
| `mdns` | All multicast DNS traffic |
| `mdns and dns.qry.name contains "_http._tcp"` | mDNS service discovery for HTTP |
| `mdns and dns.qry.name contains "_airplay"` | AirPlay device discovery |
| `mdns and dns.qry.name contains "_printer"` | Printer discovery |
| `dns.qry.name matches "\\._tcp\\.local$"` | All mDNS TCP service queries |
| `llmnr` | Link-Local Multicast Name Resolution (Windows) |
| `llmnr.qry_name` | Names being resolved via LLMNR (recon: Windows host inventory) |
| `ssdp` | SSDP / UPnP discovery (recon: IoT and consumer devices) |
| `udp.port == 1900` | SSDP by port |
| `http.request.method == "M-SEARCH"` | SSDP discovery requests |

---

## 19. VLAN / Tunneling

| Filter | Purpose |
|---|---|
| `vlan` | Any 802.1Q-tagged frame |
| `vlan.id == 100` | Specific VLAN ID |
| `vlan.priority > 4` | High-priority VLAN frames |
| `gre` | GRE-tunneled traffic |
| `mpls` | MPLS-labeled traffic |
| `mpls.label == 100` | Specific MPLS label |
| `pppoe` | PPP over Ethernet |
| `vxlan` | VXLAN overlay |
| `vxlan.vni == 5000` | Specific VXLAN network identifier |

---

## 20. Wireless (802.11)

> Only useful on captures taken in monitor mode. Standard Windows Wi-Fi captures won't expose most of these.

| Filter | Purpose |
|---|---|
| `wlan` | All 802.11 frames |
| `wlan.fc.type == 0` | Management frames |
| `wlan.fc.type == 1` | Control frames |
| `wlan.fc.type == 2` | Data frames |
| `wlan.fc.type_subtype == 0x08` | Beacon frames (recon: AP discovery) |
| `wlan.fc.type_subtype == 0x04` | Probe requests (recon: client SSID history) |
| `wlan.fc.type_subtype == 0x05` | Probe responses |
| `wlan.fc.type_subtype == 0x0b` | Authentication frames |
| `wlan.fc.type_subtype == 0x00` | Association requests |
| `wlan.sa == aa:bb:cc:dd:ee:ff` | Source MAC of a frame |
| `wlan.bssid == aa:bb:cc:dd:ee:ff` | BSSID (AP MAC) |
| `wlan.ssid == "MyNetwork"` | SSID match |
| `wlan_radio.signal_dbm > -60` | Strong signal frames |
| `eapol` | WPA/WPA2 EAPOL handshake frames |

---

## 21. Recon-Specific Combined Filters

| Filter | Purpose |
|---|---|
| `arp or icmp or mdns or nbns or llmnr or dhcp or ssdp` | Local discovery omnibus (all common broadcast/multicast chatter) |
| `tcp.flags.syn == 1 and tcp.flags.ack == 0` | New TCP connection attempts (recon: scan detection or initiation) |
| `tcp.flags.syn == 1 and tcp.flags.ack == 1` | Accepted handshakes (recon: open ports) |
| `tcp.flags.reset == 1 and tcp.flags.ack == 1` | RST-ACK (recon: closed/refused ports) |
| `icmp.type == 3 and icmp.code == 3` | Port unreachable (recon: closed UDP port) |
| `tls.handshake.type == 1` | TLS Client Hellos (recon: every HTTPS destination, SNI visible) |
| `tls.handshake.type == 11` | Certificate exchanges (recon: cert content reveals issuer/subject) |
| `http.user_agent or http.server` | Banner-rich HTTP packets (recon: client and server fingerprints) |
| `dns.qry.type in {1 28 15 2 16}` | A, AAAA, MX, NS, TXT queries (recon: full infrastructure discovery) |
| `smb.native_os or smb.native_lanman or http.server or ssh.protocol or ftp.response.code == 220` | All-purpose banner grab across protocols |
| `dhcp.option.hostname or nbns.name or mdns or llmnr.qry_name` | Hostname-revealing traffic (recon: device inventory by name) |
| `kerberos.CNameString or smb.user or ldap.name` | Username-leaking traffic (recon: AD account enumeration) |
| `tcp.port in {21 22 23 25 80 110 139 143 443 445 3306 3389 5900 8080}` | Common service-port traffic only |
| `ip.ttl == 64 or ip.ttl == 128 or ip.ttl == 255` | Default TTLs (recon: OS family guesses — Linux/Win/Cisco) |
| `not (ip.dst == 224.0.0.0/4 or eth.dst == ff:ff:ff:ff:ff:ff)` | Suppress all broadcast/multicast (focus on unicast conversations) |

---

## 22. Troubleshooting / Anomaly Filters

| Filter | Purpose |
|---|---|
| `tcp.analysis.flags` | Any Wireshark-flagged TCP issue |
| `tcp.analysis.retransmission or tcp.analysis.fast_retransmission` | Retransmissions |
| `tcp.analysis.duplicate_ack` | Dup ACKs (loss indicator) |
| `tcp.analysis.zero_window` | Receiver paused |
| `tcp.analysis.window_full` | Sender hit window limit |
| `tcp.analysis.out_of_order` | Out-of-order delivery |
| `tcp.analysis.lost_segment` | Detected missing segment |
| `tcp.analysis.keep_alive` | Keep-alive probes |
| `tcp.flags.reset == 1` | Connection resets |
| `dns.flags.rcode != 0` | DNS errors of any kind |
| `expert.severity == error` | Wireshark "expert" error level |
| `expert.severity == warn` | Expert warnings |
| `_ws.malformed` | Malformed packets |
| `frame.time_delta > 1` | Packets arriving >1s after the previous |
| `tcp.time_delta > 0.5` | TCP packets with large inter-arrival gaps |
| `ip.checksum_bad == 1` | Bad IP checksums (rare; often offload-related) |
| `tcp.checksum_bad == 1` | Bad TCP checksums |

---

## Tips for Building Filters Quickly

- **Right-click any field** in the packet details pane → **Apply as Filter → Selected**. This auto-generates the correct filter syntax for that exact field value. Fastest way to discover field names.
- **Analyze → Display Filter Expression** opens a browsable tree of every known field grouped by protocol.
- **Bookmark filters** with the bookmark icon next to the filter bar.
- **Save useful filters** as buttons via the `+` icon at the right of the filter bar — they appear as clickable shortcuts.
- **Combine with display filter macros** for reusable named expressions (Analyze → Display Filter Macros).
- **Filter bar colors**: green = valid syntax, red = invalid, yellow = valid but suspicious (e.g., `ip.addr != 1.1.1.1` evaluates differently than expected — usually means "and not", which is rarely what you want; consider `not ip.addr == 1.1.1.1`).
