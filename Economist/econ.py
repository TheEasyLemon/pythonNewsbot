"""#!/usr/bin/env python"""

import requests
import datetime
from bs4 import BeautifulSoup
import time
import re
from lib.citation import Citation
from lib.datafinder import Datafinder

# XML Parse

# the below syntax eliminates the need to close the file
# get last read day, last_opened is year, month, day
with open("info.txt", "r") as txt:
    lines = txt.readlines()
line = lines[0]
last_opened = line.split()

# get current read string
now = datetime.datetime.now()

# write current read as last read for the file

quarter = (now.month-1)//3 + 1

with open("info.txt", "w") as txt:
    txt.write(str(now.year) + " " + str(quarter) + "\n")
    # replaces all previous lines
    for n in lines:
        if n != line:
            txt.write(n)

# get list of xml sitemaps to parse
xml_maps = []

# previous and current quarter.
for i in range(int(last_opened[1]), quarter + 1):
    xml_maps.append("https://www.economist.com/sitemap-" + str(now.year) + "-Q" +
                    str(quarter) + ".xml")
    # https://www.economist.com/sitemap-(year)-Q(quarter number).xml

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
    # if the url is actually an article
    for tag in loc:
        if str(now.month) in tag.string:
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
        
        path = ("/Users/dawsonren/Documents/pythonNewsbot/News/Econ/" +
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
                file.write("Source: The Economist")
                print("Successful Extraction %s" % citation.title)
        except FileNotFoundError:
            print("\nFile not found.\n")
