import nmap
import json

# Code
scanner = nmap.PortScanner()
network = '192.168.1.0/24'
network = '192.168.100.0/24'
arguments = '-n -sn -PE -PA21,23,80,3389'
arguments = '-n -sn'

# Info about hosts
scanner.scan(hosts=network, arguments=arguments)
hosts_list = [(host, scanner[host]['status']['state'], scanner[host].hostname()) for host in scanner.all_hosts()]
for host, status, hostname in hosts_list:
    print(f"{host:15} : {status:4} : {hostname}")