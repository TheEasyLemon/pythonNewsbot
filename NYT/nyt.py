import requests
import datetime
from bs4 import BeautifulSoup
import time
import re
import dateutil
from dateutil import parser as date_parser
from lib.citation import Citation
from lib.datafinder import Datafinder
import urllib.request
import io
import gzip

# XML Parse

# Dictionary of days in each month

days_in_month = {
    1: 31,
    2: 28,
    3: 31,
    4: 30,
    5: 31,
    6: 30,
    7: 31,
    8: 31,
    9: 30,
    10: 31,
    11: 30,
    12: 31
}

# the below syntax eliminates the need to close the file
# get last read day, last_opened is year and month
with open("info.txt", "r") as txt:
    lines = txt.readlines()
line = lines[0]
last_opened = line.split()
#last_opened[0] is year, last_opened[1] is month

# get current read string
now = datetime.datetime.now()

# write current read as last read for the file
'''
with open("info.txt", "w") as txt:
    txt.write(str(now.year) + " " + str(now.month) + "\n")
    # replaces all previous lines
    for n in lines:
        if n != line:
            txt.write(n)
'''
# function to add zeroes
def add_zeroes(num):
    if (num < 10):
        return "0" + str(num)
    return str(num)


# Gets XML Sitemaps - assume current month is what we're parsing...
# this might result in many duplicates as more than one tournament per month
xmlSitemap = ("https://www.nytimes.com/sitemaps/www.nytimes.com/sitemap_" + last_opened[0] + "_" +
       last_opened[1] + ".xml.gz")

print(xmlSitemap)

# TODO: Fix this...

# Unzip Gunzip (.gz) file

# Make XML Request
response = urllib.request.urlopen(xmlSitemap)
compressed_file = io.BytesIO(response.read())
decompressed_file = gzip.GzipFile(fileobj=compressed_file)

byteData = gzip.decompress(compressed_file)

print(type(byteData))
print(byteData)


'''
# Turns HTML Article Soup into Citation Object, container for data
# found by Datafinder

def soup_to_citation(url, soup):
    df = Datafinder(soup)

    citation = Citation()
    citation.authors = df.get_authors()
    citation.title = df.get_title()
    citation.access_date = datetime.datetime.now()
    citation.publication_date = df.get_publication_date()
    citation.url = url
    citation.data = df.get_content()
    return citation

# parsing xml sitemaps
print("Attempting %s extraction..." % url)

sitemap_soup = BeautifulSoup(sitemap.text, "html.parser")
loc = sitemap_soup.find_all("loc")
sitemap_urls = []

# if the url is actually an article
for tag in loc:
    if ("news" in tag.string) and (str(last_opened[1]) in tag.string):
        sitemap_urls.append(tag.string)

# HTML Parse - make requests to each url, cite each source

for article_url in sitemap_urls:
    article = requests.get(article_url)
    if article.status_code == 404:
        print("Article @ %s not real" % article_url)       
    citation = soup_to_citation(article_url,
                                BeautifulSoup(article.text,
                                              "html.parser"))

    format_title = "".join(citation.title.split()).replace("/", "")
    
    path = ("/Users/dawsonren/Documents/pythonNewsbot/News/" +
            format_title + ".txt")

    try:
        with open(path, "w") as file:
            file.write("Title: " + citation.title + "\n\n")
            file.write("URL: " + citation.url + "\n\n")
            file.write("Article: " + "\n\n")
            for line in citation.data:
                chunks = line.split(" ")
                count = 0
                temp = ""
                for word in chunks:
                    temp += word
                    temp += " "
                    if count == 12:
                        temp += "\n"
                    count += 1
                file.write(temp)
            file.write("\nPublication Date: " +
                       str(citation.publication_date) + "\n\n")
            file.write("Source: Al Jazeera")
            print("Successful Extraction %s" % citation.title)
    except FileNotFoundError:
        print("\nFile not found.\n")
'''

