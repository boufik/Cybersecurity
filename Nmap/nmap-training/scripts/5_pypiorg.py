import nmap
import json

# Code
scanner = nmap.PortScanner()
host1 = '192.168.1.180'
host1 = '192.168.100.93'
host2 = '172.17.0.4'
hosts = f"{host1} {host2}"
arguments = '-sS -sV -p-'

# Info about hosts
result = scanner.scan(hosts=hosts, arguments=arguments)
all_hosts = scanner.all_hosts()
for host in all_hosts:
    print(80*"-")
    print(f"Host IP: {host}")
    print(f"Hostname: {scanner[host].hostname()}")
    print(f"Host state: {scanner[host].state()}")
    for proto in scanner[host].all_protocols():
        print(f"\nProtocol: {proto}")
        ports = list(scanner[host][proto].keys())
        ports.sort()
        for port in ports:
            print(f"port: {port:5}\tstate: {scanner[host][proto][port]["state"]}")
    print(80*'-')
    print("\n")