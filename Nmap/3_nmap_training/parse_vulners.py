import re

"""
filename = "../outputs/scripts_vulners.txt"
with open(filename, "r") as file:
    text = file.read()
"""

def find_CVEs_CNVDs(text):
    text = str(text)
    CVE_list = re.findall(r'CVE-\d{4}-\d+', text)
    CNVD_list = re.findall(r'CNVD-\d{4}-\d+', text)
    CVE_list = sorted(list(set(CVE_list)))
    CNVD_list = sorted(list(set(CNVD_list)))
    return CVE_list, CNVD_list

def find_CVEs(text):
    text = str(text)
    CVE_list = re.findall(r'CVE-\d{4}-\d+', text)
    CVE_list = sorted(list(set(CVE_list)))
    return CVE_list