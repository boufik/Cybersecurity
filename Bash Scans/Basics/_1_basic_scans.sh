# 1. Unconfigured scan
nmap scanme.nmap.org
 
# 2. TCP Connect Scan and Service Probe Scan (in a single command)
nmap -sT -sV scanme.nmap.org
 
# 3. TCP Connect Scan and Service Probe Scan with Configuration Options
# Add flag -A: Enable OS detection, version detection, script scanning, and traceroute
nmap -sT -sV -A scanme.nmap.org
 
# 4. Verbose and output results in XML format
nmap -vv -oX XMLReport scanme.nmap.org
 
# 5. Diplay the created file
more XMLReport
