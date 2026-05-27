import nmap
import json
import re
from parse_vulners import *
from parse_sql_inject import find_links




# Scanner object and flags/options
scanner = nmap.PortScanner()
targets = '172.17.0.1 172.17.0.2 172.17.0.3 172.17.0.4'
arguments = '-p- -sV --reason -O --osscan-guess --script=vulners,default,banner,vuln,version'
targets = '172.17.0.4'
arguments = '-p- -sV --reason -O --osscan-guess --script=vulners,default,vuln'
result = scanner.scan(hosts=targets, arguments=arguments)
dashes = 100 * '~'
# print(json.dumps(result, indent=4))




# Regarding the dictionary result["scan"]
print("\n-------- ALL --------\n\n")
dct = result["scan"]
non_interested = ["closed"]
for host in dct:


    # Initialization
    host_state = dct[host]["status"]["state"]
    reason = dct[host]["status"]["reason"]
    document = dict()                               # Host-specific
    scripts = dict()                                # Host-specific, but afterwards it also becomes port-specific as well
    document_truncated = dict()
    scripts_truncated = dict()
    vulnerabilities_CVEs = list()
    vulnerabilities_CNVDs = list()
    sql_injections = list()

    # 0) BASICS
    document["IP"] = host
    document["IP_version"] = "ToBeDefinedInFuture"
    document["FQDN"] = dct[host]["hostnames"][0]["name"]
    document_truncated["IP"] = host
    document_truncated["IP_version"] = "ToBeDefinedInFuture"
    document_truncated["FQDN"] = dct[host]["hostnames"][0]["name"]


    # 2) PORTS and SERVICES + SCRIPTS and VULNERABILITIES
    document["services"] = list()
    document_truncated["services"] = list()
    if host_state.lower() == "up":
        print(f"{dashes}\n{dashes}\n\n")
        print(f"> Host {host} is {host_state} ({reason}).\n")
        
        # TCP protocol ports
        if "tcp" in dct[host]:
            tcp_protocols_dict = dct[host]["tcp"]
            for tcp_port in tcp_protocols_dict:
                port_state = dct[host]["tcp"][tcp_port]["state"]
                if port_state not in non_interested:
                    # 2) PORTS and SERVICES
                    name = dct[host]["tcp"][tcp_port]["name"]
                    product_version = dct[host]["tcp"][tcp_port]["product"] + " " + dct[host]["tcp"][tcp_port]["version"]
                    cpe = dct[host]["tcp"][tcp_port]["cpe"]
                    service = {"port": tcp_port, "protocol": "tcp", "state": port_state, "name": name, "product_version": product_version, "cpe": cpe}
                    document["services"].append(service)
                    document_truncated["services"].append(service)
                    # 4) SCRIPTS and VULNERABILITIES
                    scripts[tcp_port] = dict()
                    scripts_truncated[tcp_port] = dict()
                    if "script" in dct[host]["tcp"][tcp_port]:
                        scripts_dict_nmap = dct[host]["tcp"][tcp_port]["script"]
                        for script, value in scripts_dict_nmap.items():
                            # 4a) Differentiate the content of key named "scripts"
                            scripts[tcp_port][script] = value
                            if len(value) > 50:
                                scripts_truncated[tcp_port][script] = value[:50]
                            else:
                                scripts_truncated[tcp_port][script] = value
                            # 4b) Special script cases to populate more data
                            if script == "vulners":
                                CVE_list, CNVD_list = find_CVEs_CNVDs(value)
                                vulnerabilities_CVEs += CVE_list
                                vulnerabilities_CNVDs += CNVD_list
                            elif script == "http-sql-injection":
                                links = find_links(value)
                                sql_injections += links
                            elif "CVE-" in value.upper():
                                more_cves = re.findall(r'CVE-\d{4}-\d+', value)
                                vulnerabilities_CVEs += more_cves
                            
                
                document["vulnerabilities_CVEs"] = vulnerabilities_CVEs
                document["vulnerabilities_CNVDs"] = vulnerabilities_CNVDs
                document["sql_injections"] = sql_injections
                document_truncated["vulnerabilities_CVEs"] = vulnerabilities_CVEs
                document_truncated["vulnerabilities_CNVDs"] = vulnerabilities_CNVDs
                document_truncated["sql_injections"] = sql_injections
                # Differentiate in the key named "scripts"
                document["scripts"] = scripts
                document_truncated["scripts_truncated"] = scripts_truncated

        # UDP protocols ports
        if "udp" in dct[host]:
            udp_protocols_dict = dct[host]["udp"]
            for udp_port in udp_protocols_dict:
                port_state = dct[host]["udp"][udp_port]["state"]
                if port_state not in non_interested:
                    # 2) PORTS and SERVICES
                    name = dct[host]["udp"][udp_port]["name"]
                    product_version = dct[host]["udp"][udp_port]["product"] + " " + dct[host]["udp"][udp_port]["version"]
                    cpe = dct[host]["udp"][udp_port]["cpe"]
                    service = {"port": udp_port, "protocol": "udp", "state": port_state, "name": name, "product_version": product_version, "cpe": cpe}
                    document["services"].append(service)
                    document_truncated["services"].append(service)
                    # 4) SCRIPTS and VULNERABILITIES
                    scripts[udp_port] = dict()
                    scripts_truncated[udp_port] = dict()
                    if "script" in dct[host]["udp"][udp_port]:
                        scripts_dict_nmap = dct[host]["udp"][udp_port]["script"]
                        for script, value in scripts_dict_nmap.items():
                            # 4a) Differentiate the content of key named "scripts"
                            scripts[udp_port][script] = value
                            if len(value) > 50:
                                scripts_truncated[udp_port][script] = value[:50]
                            else:
                                scripts_truncated[tcp_port][script] = value
                            # 4b) Special script cases to populate more data
                            if script == "vulners":
                                CVE_list, CNVD_list = find_CVEs_CNVDs(value)
                                vulnerabilities_CVEs += CVE_list
                                vulnerabilities_CNVDs += CNVD_list
                            elif script == "http-sql-injection":
                                links = find_links(value)
                                sql_injections += links
                            elif "CVE-" in value.upper():
                                more_cves = re.findall(r'CVE-\d{4}-\d+', value)
                                vulnerabilities_CVEs += more_cves
                            
                
                document["vulnerabilities_CVEs"] = vulnerabilities_CVEs
                document["vulnerabilities_CNVDs"] = vulnerabilities_CNVDs
                document["sql_injections"] = sql_injections
                document_truncated["vulnerabilities_CVEs"] = vulnerabilities_CVEs
                document_truncated["vulnerabilities_CNVDs"] = vulnerabilities_CNVDs
                document_truncated["sql_injections"] = sql_injections
                # Differentiate in the key named "scripts"
                document["scripts"] = scripts
                document_truncated["scripts_truncated"] = scripts_truncated

    
    # 3) OPERATING SYSTEM
    document["os"] = dict()
    document_truncated["os"] = dict()
    # osmatch is a list
    osmatch = dct[host]["osmatch"]
    if osmatch:
        # If osmatch exists, it is a list
        osmatch = osmatch[0]
        guess = osmatch["name"]
        document["os"]["guess"] = guess
        document_truncated["os"]["guess"] = guess
        if "osclass" in osmatch:
            osclass = osmatch["osclass"]    # List
            osfamilies = list()
            cpes = list()
            for obj in osclass:
                osfamilies.append(obj["osfamily"] + " " + obj["osgen"])
                cpes.append(obj["cpe"][0])
            osfamily_range = " | ".join(osfamilies)
            cpe_range = " | ".join(cpes)
            document["os"]["osfamily"] = osfamily_range
            document_truncated["os"]["osfamily"] = osfamily_range
            document["os"]["cpe"] = cpe_range
            document_truncated["os"]["cpe"] = cpe_range


    # Prefer to print out the truncated document, NOT the original one
    print(f"{json.dumps(document_truncated, indent=4)}\n{dashes}\n{dashes}\n\n")