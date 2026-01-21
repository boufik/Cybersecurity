import nmap
import json

# Code
scanner = nmap.PortScanner()
hosts = '127.0.0.1'
arguments = '-sS -sV -p-'
result = scanner.scan(hosts=hosts, arguments=arguments)

# Prints
scaninfo = scanner.scaninfo()
scaninfo2 = result["nmap"]["scaninfo"]
print(f"Scan info: {scaninfo}")
print(f"Scan info: {scaninfo2}\n")
print(f"type(result) = {type(result)}")
print(f"type(scanner) = {type(scanner)}")