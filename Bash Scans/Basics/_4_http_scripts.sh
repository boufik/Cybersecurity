# 1. Scan port 80 (HTTP) + http-date script
nmap -p80 --script http-date scanme.nmap.org

# 2. Scan port 8000 (HTTP alternate port) + http-date script
nmap -p8000 --script http-date scanme.nmap.org

# 3. Scan port 80 + http-csrf (Cross-Site Request Forgery: A common web vulnerability)
nmap -p80 --script http-csrf scanme.nmap.org

# 4. Scan port 80 + http-backup-finder (Checks if the web server reveals any backup files)
nmap -p80 --script http-backup-finder scanme.nmap.org
