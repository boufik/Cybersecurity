import nmap
import json

# Basics
scanner = nmap.PortScanner()
targets = '172.17.0.1 172.17.0.2 172.17.0.3 172.17.0.4'
arguments = '-p- -sV --reason --script=version'
result = scanner.scan(hosts=targets, arguments=arguments)
# print(f"result = {type(result)}\n", json.dumps(result, indent=4))

# result["scan"] = dictionary
print("\n-------- Service Enumeration --------\n\n")
dct = result["scan"]
non_interested = ["closed"]
for host in dct:
    host_state = dct[host]["status"]["state"]
    reason = dct[host]["status"]["reason"]
    document = dict()
    document["IP"] = host
    document["IP_version"] = "ToBeDefinedInFuture"
    document["FQDN"] = dct[host]["hostnames"][0]["name"]
    document["services"] = list()
    # If the host is up
    if host_state.lower() == "up":
        print(f"> Host {host} is {host_state} ({reason}).\n")
        # TCP protocol ports
        if "tcp" in dct[host]:
            tcp_protocols_dict = dct[host]["tcp"]
            for tcp_port in tcp_protocols_dict:
                port_state = dct[host]["tcp"][tcp_port]["state"]
                if port_state not in non_interested:
                    name = dct[host]["tcp"][tcp_port]["name"]
                    product_version = dct[host]["tcp"][tcp_port]["product"] + " " + dct[host]["tcp"][tcp_port]["version"]
                    cpe = dct[host]["tcp"][tcp_port]["cpe"]
                    service = {"port": tcp_port, "protocol": "tcp", "state": port_state, "name": name, "product_version": product_version, "cpe": cpe}
                    document["services"].append(service)
        # UDP protocols ports
        if "udp" in dct[host]:
            udp_protocols_dict = dct[host]["udp"]
            for udp_port in udp_protocols_dict:
                port_state = dct[host]["udp"][udp_port]["state"]
                if port_state not in non_interested:
                    name = dct[host]["udp"][udp_port]["name"]
                    product_version = dct[host]["udp"][udp_port]["product"] + " " + dct[host]["udp"][udp_port]["version"]
                    cpe = dct[host]["udp"][udp_port]["cpe"]
                    service = {"port": udp_port, "protocol": "udp", "state": port_state, "name": name, "product_version": product_version, "cpe": cpe}
                    document["services"].append(service)
    print(json.dumps(document, indent=4), '\n\n')