# 1. Unconfigured scan
nmap localhost

# 2. Scan port 22 (SSH) with service version + default scripts
nmap -p22 -sV -sC localhost

# 3. Run ssh script
nmap --script ssh-publickey-acceptance localhost

# 4. Run ssh auth methods script
nmap --script ssh-auth-methods localhost
