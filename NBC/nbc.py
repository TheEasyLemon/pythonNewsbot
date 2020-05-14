'''#!/usr/bin/env python'''

# python imports
import requests
import datetime

# native imports
from bs4 import BeautifulSoup

# native module imports
from lib.citation import Citation
from lib.datafinder import Datafinder

"""
Scrapes a news article for its article files based on the stipulations in
Datafinder, formatting based on the stipulations in Citation.

Reuters provides one XML file for each day.

Each URL is scraped according to Datafinder and stored in a Citation object.
This information is then loaded into a .txt file.

This file is not meant to be run separately. It is a template
that provides functions that can be implemented.
"""

def getUpdateLastOpened(test = False, file_name = "date.txt"):
    """(file_name = str, test = False) => (tuple of int)
    Parses the file_name for its first line, which should contain
    the date last opened in year, month, day format.

    Then writes the new date back into the file, unless test is True.
    
    ex. "2020,3,7" => (2020, 3, 7)
    """
    
    # read last opened date
    with open(file_name, "r") as txt:
        line = txt.readline()
    last_opened = line.split(",")

    # get current date
    now = datetime.datetime.now()

    # only update if test is False
    if not test:
        with open(file_name, "w+") as txt:
            txt.write(f"{now.year},{now.month}.{now.day}")

    # return tuple of dates
    return (int(last_opened[0]), int(last_opened[1]), int(last_opened[2]))

def soup_to_citation(url, soup):
    """(str, Soup object) => Citation object

    Parses the soup from the url through the Datafinder. Stores the data
    in the Citation object, which is returned.

    """
    
    df = Datafinder(soup)

    citation = Citation()
    citation.authors = df.get_authors()
    citation.title = df.get_title()
    citation.access_date = datetime.datetime.now()
    citation.publication_date = df.get_publication_date()
    citation.url = url
    citation.data = df.get_content()
    return citation

def parseSitemap(sitemap_url, url_matches):
    """(str, [list of str],) => list of str

    Requests the sitemap. Then, turns it into soup and finds all
    of the article URLs. Checks these URLs against url_matches to see
    if it is relevant.
    
    """
    
    # request xml sitemap
    print(f"Attempting {sitemap_url} extraction...")
    sitemap = requests.get(sitemap_url)

    # check if the connection status is stable
    if sitemap.status_code == 404:
        print(f"XML Sitemap @ {sitemap_url} not real")
        return
    elif sitemap.status_code == 200:
        print(f"Successful XML Extraction {sitemap_url}")
    else:
        print(f"Unknown error code. {sitemap.status_code}")
        return

    # convert sitemap text into soup
    sitemap_soup = BeautifulSoup(sitemap.text, "html.parser")

    # find all instances of loc
    loc = sitemap_soup.find_all("loc")
    sitemap_urls = set()

    # check if any of the strings in url_matches is in the article url
    for article in loc:
        for match in url_matches:
            if match in article.string:
                sitemap_urls.add(article.string)

    return list(sitemap_urls)

def urltofile(article_url, last_opened, news_agency, test = False):
    """(str, (tuple of int), bool, str) => None

    Converts a url from Reuters into a file and stores it inside path.

    If test = True, it will not write to file.

    Needs news_agency for storage purposes.

    """
    # request article
    article = requests.get(article_url)
    
    if article.status_code == 404:
        print("Article @ %s not real" % article_url)

    # convert to citation object
    citation = soup_to_citation(article_url,
                                BeautifulSoup(article.text,
                                              "html.parser"))

    # rids the title of any slashes
    format_title = "".join(citation.title.split()).replace("/", "")

    # relative path to news agency folder
    path = (f"../News/{news_agency}/" + format_title + ".txt")

    if not test:
        with open(path, "w+") as file:
            file.write("Title: " + citation.title + "\n\n")
            file.write("URL: " + citation.url + "\n\n")
            file.write("Article: " + "\n\n")
            file.write(citation.data)
            file.write("\nPublication Date: " +
                       str(citation.publication_date) + "\n\n")
            file.write(f"Source: {news_agency}")
        print(f"Successful Extraction {citation.title}")
        return

    print(f"{citation.title}")


def main():
    name = "NBC"
    # test determines whether or not it will write to a file
    select = input("Test? Y/N")
    if select == "Y":
        t = True
    elif select == "N":
        t = False
    else:
        return

    last_opened = getUpdateLastOpened(test = t)

    now = datetime.datetime.now()

    # parse all of the past and present month's XML sitemaps
    for i in range(int(last_opened[1]), now.month + 1):
        xmlurl = f"https://www.nbcnews.com/sitemap/nbcnews/sitemap-{now.year}-{i:02d}-article.xml"
        urlmatches = ["news", "indepth", "ajimpact"] 

        # get list of article_urls from sitemap
        article_urls = parseSitemap(xmlurl, urlmatches)

        # scrape each article
        for article_url in article_urls:
            urltofile(article_url, last_opened, name, test = t, )

    print("Program finished.")

if __name__ == "__main__":
    main()
