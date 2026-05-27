import re

"""
filename = "../outputs/scripts_sql_inject.txt"
with open(filename, "r") as file:
    text = file.read()
"""

def find_links(text):
    text = str(text)
    words = text.split(" ")
    links = list()
    for word in words:
        if word and word[:4] == "http":
            # Trim the "\n" in the end of the word --> First, remove "n" and then "/"
            """
            if word[-1] == "n":
                word = word[:-1]
                word = word[:-1]
            """
            alphabet = "abcdefghijklmnopqrstuvwxyz0123456789_"
            if word[-2] not in alphabet:
                word = word[:-2]
            links.append(word)
    links = list(set(links))
    return links