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
print(scanner.csv())