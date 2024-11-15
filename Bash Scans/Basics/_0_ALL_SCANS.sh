# 1. Basic/unconfigured scan
nmap localhost

# 2. Aggressive scan
nmap -A localhost

# 3. Specific port scan (here 8025)
nmap -p8025 localhost

# 4. TCP connect scan
nmap -sT localhost

# 5. TCP SYN scan - A stealth scan that reduces the probability of being detected - Requires elevated/root privileges - Use "sudo"
sudo nmap -sS localhost

# 6. UDP scan - Requires elevated/root privileges - Use "sudo"
sudo nmap -sU localhost

# 7. Ping sweep - Search for active hosts / IP addresses in a network - Sending ICMP packets
nmap -sn 192.168.1.1-255
