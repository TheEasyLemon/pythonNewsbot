"""#!/usr/bin/env python"""

import requests
import datetime
from bs4 import BeautifulSoup
import time
import re
from lib.citation import Citation
from lib.datafinder import Datafinder

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
# get last read day, last_opened is year, month, day
with open("info.txt", "r") as txt:
    lines = txt.readlines()
line = lines[0]
last_opened = line.split()

# get current read string
now = datetime.datetime.now()

# function to add zeroes
def add_zeroes(num):
    if (num < 10):
        return "0" + str(num)
    return str(num)

# write current read as last read for the file

with open("info.txt", "w") as txt:
    txt.write(str(now.year) + " " + str(now.month) +
             " " + str(now.day) + "\n")
    # replaces all previous lines
    for n in lines:
        if n != line:
            txt.write(n)

# get list of xml sitemaps to parse
xml_maps = []

# last months, excluding this month. Doesn't get the days between months...
for i in range(int(last_opened[1]), now.month):
    for j in range(int(last_opened[2]), days_in_month[i]):
        xml_maps.append("https://www.brookings.edu/sitemap-" +
                        str(now.year) + ".xml?mm=" + add_zeroes(i) +
                        "&dd=" + add_zeroes(j))
        #https://www.brookings.edu/sitemap-(year).xml?mm=(month)&dd=(day)

# this month
for k in range(int(last_opened[2]), now.day):
    xml_maps.append("https://www.brookings.edu/sitemap-" +
                        str(now.year) + ".xml?mm=" + add_zeroes(now.month) +
                        "&dd=" + add_zeroes(k))
    #https://www.brookings.edu/sitemap-(year).xml?mm=(month)&dd=(day)

for url in xml_maps:
    print("Found: " + url)

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

# obtaining xml sitemaps
for url in xml_maps:
    print("Attempting %s extraction..." % url)
    sitemap = requests.get(url)
    if sitemap.status_code == 404:
        print("XML Sitemap @ %s not real" % url)
    elif sitemap.status_code == 200:
        print("Successful Extraction %s" % sitemap)
    
    sitemap_soup = BeautifulSoup(sitemap.text, "html.parser")
    loc = sitemap_soup.find_all("loc")
    sitemap_urls = []
    # if the url is actually an article that we want
    for tag in loc:
        if "blog" or "testimonies" in tag.string:
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
        
        path = ("/Users/dawsonren/Documents/pythonNewsbot/News/Brookings/" +
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
                file.write("Source: Brookings Institute")
                print("Successful Extraction %s" % citation.title)
        except FileNotFoundError:
            print("\nFile not found.\n")


