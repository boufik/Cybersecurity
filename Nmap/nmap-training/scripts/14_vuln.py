import nmap
import json
from parse_vulners import find_CVEs
from parse_sql_inject import find_links


# Basics
scanner = nmap.PortScanner()
targets = '172.17.0.4'
arguments = '-sV --script=default,vuln'
result = scanner.scan(hosts=targets, arguments=arguments)
# print(f"result = {type(result)}\n", json.dumps(result, indent=4))

# result["scan"] = dictionary
non_interested = ["closed"]
dct = result["scan"]
for host in dct:
    print(f"> Host {host}")
    host_state = dct[host]["status"]["state"]
    document = dict()
    scripts = dict()
    document["IP"] = host
    document["IP_version"] = "ToBeDefinedInFuture"
    document["FQDN"] = dct[host]["hostnames"][0]["name"]
    if host_state.lower() == "up":
        print(f"Host {host} is {host_state}.\n")
        # TCP protocol ports
        if "tcp" in dct[host]:
            tcp_protocols_dict = dct[host]["tcp"]
            for tcp_port in tcp_protocols_dict:
                port_state = dct[host]["tcp"][tcp_port]["state"]
                if port_state not in non_interested:
                    scripts[tcp_port] = dict()
                    scripts_dict = dct[host]["tcp"][tcp_port]["script"]
                    for script, value in scripts_dict.items():
                        if script == "vulners":
                            CVE_list, CNVD_list = find_CVEs(value)
                            scripts[tcp_port][script] = CVE_list
                        elif script == "http-sql-injection":
                            scripts[tcp_port][script] = find_links(value)
                        else:
                            scripts[tcp_port][script] = value
                document["scripts"] = scripts
        # UDP protocol ports
        if "udp" in dct[host]:
            udp_protocols_dict = dct[host]["udp"]
            for udp_port in udp_protocols_dict:
                port_state = dct[host]["udp"][udp_port]["state"]
                if port_state not in non_interested:
                    scripts[udp_port] = dict()
                    scripts_dict = dct[host]["udp"][udp_port]["script"]
                    for script, value in scripts_dict.items():
                        if script == "vulners":
                            CVE_list, CNVD_list = find_CVEs(value)
                            scripts[udp_port][script] = CVE_list
                        elif script == "http-sql-injection":
                            scripts[udp_port][script] = find_links(value)
                        else:
                            scripts[udp_port][script] = value
                document["scripts"] = scripts
    print(json.dumps(document, indent=4), '\n\n')
