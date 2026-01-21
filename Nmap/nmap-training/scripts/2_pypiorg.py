import nmap
import json

scanner = nmap.PortScanner()
hosts = '172.17.0.2,3,4'
arguments = '-sS -sV -p-'
result = scanner.scan(hosts=hosts, arguments=arguments)
print(json.dumps(result, indent=4), '\n', type(result))