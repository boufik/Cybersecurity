# theHarvester

```
theHarvester --domain google.com --source bing --limit 100 --filename google_report.json
```

# shodan

```
echo 'export SHODAN_API_KEY="....."' >> ~/.zshrc
tail -n 2 ~/.zshrc
source ~/.zshrc
echo $SHODAN_API_KEY
```

```
shodan count apache
shodan stats --facets org:3,port:3,os:2,vuln:5 "net:A.B.C.D/24"
```

# exiftool

```
exiftool lena_web.png
exiftool -DateTimeOriginal -Make -Model -Megapixels -Orientation -Flash -FaceDetect turkey2014.jpg
exiftool -DateTimeOriginal -Make -Model -Megapixels -Orientation -Flash -FaceDetect pineios.HEIC
exiftool -XMPToolkit -CreatorTool -Quality -Megapixels landscape_1.jpg
exiftool london.jpg | grep -i gps 
exiftool test.py
```

# whois

```
whois 8.8.8.8
whois amazon.com

# Basic Filtering with "grep"
whois amazon.com | grep -i registrar   			                            (works)
whois 8.8.8.8 | grep -i registrar      			                            (does NOT work ---> registrar is related to domains, NOT IPs)

# Advanced Filtering + Export
whois amazon.com | grep -i "Creation Date"  		                        ("..." because of spacebar character between the words)
whois amazon.com | grep -iE "email|phone|contact"	                      (flag "-iE" because of the OR operator)
whois amazon.com | grep -iE "email|phone|contact" > amazon_contact.txt
```

Websites:

```
https://www.whois.com/whois/
https://whois.domaintools.com/
https://who.is/
https://ipinfo.io/
```

# nslookup

Websites:
```
https://dnslookup.online/
https://www.nslookup.io/
https://mxtoolbox.com/
```

# dig

```
# Preliminary Steps
dig -h
dig -v

# Basics
dig codecademy.com						      ("A" records : Prints the codecademy-related IPs)
dig codecademy.com @8.8.8.8			  	(Select custom DNS)
dig -x 8.8.8.8							        (Reverse DNS lookup : IP to domain name)

# Dig by Record Files				
dig codecademy.com MX					      (Get  MX records from mail servers)
dig codecademy.com NS					      (Get  NS records from name servers)
dig codecademy.com TXT					    (Get TXT records from SPF + verification info)

# Options/Flags
dig +short codecademy.com				    (Get the IP only - Clean output)
dig +noall +answer codecademy.com		(Show only the answer section)

# Combining Basics + Record Files + Options
dig +short codecademy.com TXT @8.8.8.8
```

# sherlock

```
pipx install sherlock-project
which sherlock
sherlock hellokitty
sherlock user1 user2 user3
sherlock boufik --site github --site youtube --site twitter
```

# amass

Print list of sources:

```
amass enum --list > amass_list.txt
```

List all the names discovered during enumerations you have performed against `owasp.org` and stored in the `amass4owasp` graph database;

```
amass db -dir amass4owasp -names -d owasp.org
```
Retrieve the complete output for `owasp.org` and stored in the `amass4owasp` graph database:

```
amass db -dir amass4owasp -d owasp.org -show -ip
```
Passive search for subdomains on `owasp.org` - Passive is much quicker (no validation on DNS info, or Brute Force or wordlists).

```
amass enum -passive -d owasp.org
```

Specify that the Amass graph database, along with log files, will be stored at `./amass4owasp`. Display the IP address(es) it resolves names to with the `-ip` flag.
Provide Amass with the deepmagic DNS wordlist with the `-w` argument and also specify the location of the config.yaml file with `-config` and the output with `-o`.
Using the `-r` flag, we can specify the IP addresses of DNS resolvers at the command-line, while with the `-rf`, we can specify a file containing these on each line.
   
```
amass enum -active -d owasp.org -brute -w /root/dns_lists/deepmagic.com-top50kprefixes.txt -ip -dir amass4owasp -config /root/amass/config.yaml -o amass_results_owasp.txt
```

Search for subdomains using passive mode, a wordlist and the Google's DNS server `8.8.8.8`. Save the results into a `.txt` file in the Desktop.

```
amass enum -passive -d owasp.org -w /root/dns_lists/deepmagic.com-top50kprefixes.txt -r 8.8.8.8 -o ~/Desktop/amass_results_owasp.txt
```

Assume that for some reason the OWASP organization tends to create subdomains with `zzz` prefixes, such as:
* `zzz-dev.owasp.org` or `zzz-tmp.owasp.org`. Leverage the Amass hashcat-style wordlist mask feature to brute-force all the combinations of `zzz-[a-z][a-z][a-z].owasp.org` using the following command.
* We explicitly disable recursive DNS enumerations (-norecursive), as we are interested in quick results by only using the mask.

```
amass enum -d owasp.org -norecursive -wm "zzz-?l?l?l" -dir amass4owasp
```

Use information gathering techniques and data sources by default, such as reverse WHOIS:

```
amass intel -d owasp.org -whois
```

Look for organizational names with Amass which could return ASN IDs assigned to the target. Retrieved ASNs could then be fed back into Amass.

```
amass intel -org 'Example Ltd'
```

Search with ASN:

```
amass intel -active -asn 222222 -ip
```

Export options:

```
amass enum -d example.com -o example.txt
amass enum -d example.com -oJ example.json
```
