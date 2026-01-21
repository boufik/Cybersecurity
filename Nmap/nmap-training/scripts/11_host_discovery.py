import nmap
import json

# Basics
scanner = nmap.PortScanner()
network = '192.168.1.0/24'
network = '192.168.100.0/24'
arguments = '-sn -PE -PP -PS22,80,443 -PA80,443,3389,8080 -PU53,67,68,161'
result = scanner.scan(hosts=network, arguments=arguments)
# print(json.dumps(result, indent=4))

# result["nmap"] = dictionary
uphosts = result["nmap"]["scanstats"]["uphosts"]
downhosts = result["nmap"]["scanstats"]["downhosts"]
totalhosts = result["nmap"]["scanstats"]["totalhosts"]
print(f"\nTotal Hosts: {totalhosts}\nDown Hosts : {downhosts}\nUp Hosts   : {uphosts}\n\n")

# result["scan"] = dictionary
print("-------- Host Discovery --------\n\n")
dct = result["scan"]
for host in dct:
    if "mac" in dct[host]["addresses"]:
        MAC = dct[host]["addresses"]["mac"]
    hostname = dct[host]["hostnames"][0]["name"]
    state = dct[host]["status"]["state"]
    reason = dct[host]["status"]["reason"]
    vendor_dct = dct[host]["vendor"]
    if vendor_dct:
        vendor_name = next(iter(vendor_dct.values()))
    print(f"----\n{host:15}")
    print(f"{state} ({reason})")
    print(f"Hostname: {hostname}\nMAC: {MAC}")
    if vendor_dct:
        print(f"Vendor: {vendor_name}\n")