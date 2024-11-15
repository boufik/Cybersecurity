# 1. Unconfigured scan
nmap localhost

# 2. Service version scan + defaults scripts
nmap -sV -sC localhost

# 3. Scan port 8000 (previous scan proved that this is open) on target localhost + http-enum script
nmap -p8000 --script http-enum localhost

# 4. Output in a normal form
nmap -p8000 --script http-enum localhost -oN "http-enum-results"

# 5. Display
more http-enum-results
