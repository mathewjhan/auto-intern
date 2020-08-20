# https?:\/\/(www\.)?(jobs\.lever\.co)/(.*?)/(.*?)/(?:\)|\?|(apply)|\s)

import urllib.request
import re

pattern = r'https?:\/\/(www\.)?(jobs\.lever\.co)\/([0-9a-zA-z]*?)\/([0-9a-zA-z\-]*?).(?:\/|\)|\?|(apply)|\s)'

lever_scraped = open('lever_scraped.txt', 'w')
url = input("Please enter URL: ")

with urllib.request.urlopen(url) as response:
    html = response.read()
    plaintext = html.decode('utf-8')
    matches = re.finditer(pattern, plaintext)
    for match in matches:
        start = match.span()[0]
        end = match.span()[1]

        url = match.string[start:end]

        if(url[-1] in "/?)"):
            url = url[:-1]
        print(url, file=lever_scraped)

print("Finished scraping URLS!")
