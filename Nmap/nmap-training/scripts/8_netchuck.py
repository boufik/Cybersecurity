import nmap
import json

# Code
scanner = nmap.PortScanner()
network = '192.168.1.0/24'
network = '192.168.100.0/24'
arguments = '-n -sn'

# Info about hosts
result = scanner.scan(hosts=network, arguments=arguments)
print(json.dumps(result, indent=4))