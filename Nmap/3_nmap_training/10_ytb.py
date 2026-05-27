import nmap
import json

# Code
scanner = nmap.PortScanner()
begin_port = 77
end_port = 84
target = '172.17.0.4'
print(f"---- IP = {target} ----")

# Info about hosts
for port in range(begin_port, end_port):
    result = scanner.scan(target, str(port))
    state = result["scan"][target]["tcp"][port]["state"]
    print(f"Port {port} is {state}")