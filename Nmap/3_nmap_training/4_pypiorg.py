import nmap
import json

# Code
scanner = nmap.PortScanner()
host1 = '192.168.1.180'
host1 = '192.168.100.93'
host2 = '172.17.0.4'
hosts = f"{host1} {host2}"
arguments = '-sS -sV -p-'
result = scanner.scan(hosts=hosts, arguments=arguments)

# Prints
scaninfo = scanner.scaninfo()
print(f"Scan info: {scaninfo}")
all_hosts = scanner.all_hosts()
print(f"All hosts: {all_hosts}")
hostname1 = scanner[host1].hostname()
hostname2 = scanner[host2].hostname()
print(f"Hostnames:\n{host1} --> {hostname1}\n{host2} --> {hostname2}\n")

dict1 = scanner[host1]
print(f"---- About {host1} ----\n")
state = dict1.state()
all_protocols = dict1.all_protocols()
open_ports = list(dict1['tcp'].keys())
tcp_22 = dict1.has_tcp(22)
tcp_8080 = dict1.has_tcp(8080)
print(f"State: {state}")
print(f"All protocols: {all_protocols}")
print(f"Open ports: {open_ports}")
print(f"TCP 22? {tcp_22}")
print(f"TCP 8080? {tcp_8080}")