# 1. Most-used flags

| Flag | Purpose |
|---|---|
| `-D` | List interfaces |
| `-i <iface>` | Interface (number or name) for live traffic capture |
| `-r <file>` | Read from pcap file |
| `-w <file>` | Write to pcap file |
| `-c <N>` | Stop after N packets: better combined with `-i` live capture flag, since with `-r`, the flag `-c` refers to a limit when reading, not after filtering |
| `-a duration:<sec>` | Autostop after seconds |
| `-a filesize:<KB>` | Autostop after KB written |
| `-b duration:<sec>` | Ring buffer rotation interval |
| `-b filesize:<KB>` | Ring buffer file size |
| `-b files:<N>` | Ring buffer file count |
| `-f "<BPF>"` | Capture filter (BPF syntax) |
| `-Y "<display>"` | Display filter (Wireshark syntax) |
| `-T fields -e <field>` | Extract specific fields |
| `-T json` / `-T ek` / `-T pdml` | Alternate output formats |
| `-E header="y" -E separator=","` | CSV formatting for `-T fields` |
| `-V` | Verbose per-packet dissection |
| `-x` | Hex+ASCII dump |
| `-O <proto>` | Verbose only for named protocols |
| `-q` | Quiet — suppress per-packet output (use with `-z`) |
| `-z <stat>` | Run a statistics module |
| `-n` | No name resolution |
| `-N <flags>` | Selective name resolution (m/n/t/C) |
| `-t <fmt>` | Time format (a/ad/d/r/...) |
| `-l` | Line-buffered output (for live streaming) |

# 2. Top 10 recon one-liners

```powershell
# 1. List interfaces
tshark -D

# 2. Quick live capture, file output
tshark -i 1 -a duration:60 -w cap.pcapng

# 3. Open and summarize what's in a pcap
tshark -r cap.pcapng -q -z io,phs

# 4. Endpoint inventory
tshark -r cap.pcapng -q -z endpoints,ip

# 5. Unique HTTPS destinations (SNI)
tshark -r cap.pcapng -Y "tls.handshake.type == 1" -T fields -e tls.handshake.extensions_server_name | Sort-Object -Unique

# 6. Unique DNS queries
tshark -r cap.pcapng -Y "dns.flags.response == 0" -T fields -e dns.qry.name | Sort-Object -Unique

# 7. HTTP server banners
tshark -r cap.pcapng -Y "http.response and http.server" -T fields -e ip.src -e http.server | Sort-Object -Unique

# 8. Local hosts via DHCP hostnames
tshark -r cap.pcapng -Y "dhcp.option.hostname" -T fields -e dhcp.hw.mac_addr -e dhcp.option.hostname

tshark -r local_disco.pcapng -Y "mdns and dns.flags.response == 1" -T fields -e ip.src -e dns.ptr.domain_name | Sort-Object -Unique


# 9. TCP SYNs (connection attempts / scan signal)
tshark -r cap.pcapng -Y "tcp.flags.syn == 1 and tcp.flags.ack == 0" -T fields -e ip.src -e ip.dst -e tcp.dstport

# 10. CSV export of HTTP requests
tshark -r cap.pcapng -Y "http.request" -T fields -e ip.src -e http.host -e http.request.method -e http.request.uri -e http.user_agent -E header="y" -E separator="," -E quote="d" > http_requests.csv
```

# 3. Mapping between GUI and CLI

| Action | Wireshark GUI | tshark CLI |
|---|---|---|
| Pick interface | Welcome screen → double-click | `-i <N>` |
| Start capture | Shark-fin button | (the capture starts when you run the command) |
| Stop capture | Red-square button | `-c N`, `-a duration:N`, or Ctrl+C |
| Save | File → Save As | `-w file.pcapng` |
| Open | File → Open | `-r file.pcapng` |
| Display filter | Filter bar | `-Y "..."` |
| Capture filter | Capture → Options | `-f "..."` |
| Statistics → Endpoints | Menu | `-q -z endpoints,ip` |
| Statistics → Conversations | Menu | `-q -z conv,ip` |
| Statistics → Protocol Hierarchy | Menu | `-q -z io,phs` |
| Follow → TCP Stream | Right-click | `-q -z follow,tcp,ascii,<N>` |
| Add column | Right-click field → Apply as Column | `-T fields -e <field>` |
| Verbose detail of packet | Click `>` to expand | `-V` |



