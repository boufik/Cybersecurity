import nmap
import json

# Basics
scanner = nmap.PortScanner()
targets = '172.17.0.1 172.17.0.2 172.17.0.3 172.17.0.4'
arguments = '-O --osscan-guess --max-os-tries 3'
arguments = '-O --osscan-guess'
result = scanner.scan(hosts=targets, arguments=arguments)
# print(f"result = {type(result)}\n", json.dumps(result, indent=4))

# result["scan"] = dictionary
dct = result["scan"]
for host in dct:
    print(f"> Host {host}\n")
    document = dict()
    document["IP"] = host
    document["IP_version"] = "ToBeDefinedInFuture"
    document["FQDN"] = dct[host]["hostnames"][0]["name"]
    document["os"] = dict()
    # osmatch is a list
    osmatch = dct[host]["osmatch"]
    if osmatch:
        # If osmatch exists, it is a list
        osmatch = osmatch[0]
        guess = osmatch["name"]
        document["os"]["guess"] = guess
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
            document["os"]["cpe"] = cpe_range
    print(json.dumps(document, indent=4), '\n\n')