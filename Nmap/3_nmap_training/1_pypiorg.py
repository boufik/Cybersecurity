import nmap
import json

scanner = nmap.PortScanner()
result = scanner.scan('127.0.0.1', '1-10000')
print(json.dumps(result, indent=4))