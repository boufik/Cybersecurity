import nmap
import json

# Code
scanner = nmap.PortScanner()
target = '192.168.1.180'
target = '192.168.100.93'
arguments = '-p- --script vuln'

# Info about hosts
result = scanner.scan(hosts=target, arguments=arguments)
print(json.dumps(result, indent=4))