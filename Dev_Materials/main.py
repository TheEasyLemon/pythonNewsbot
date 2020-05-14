#! /usr/bin/env python3

import requests
from bs4 import BeautifulSoup
from lib.citation import Citation
from lib.formatter import APAFormatter
from lib.formatter import PolicyFormatter
from lib.datafinder import Datafinder
import datetime
import sys
import argparse
from validator_collection import validators, checkers

def url_to_soup(url):
    # Some websites are unhappy with no user agent, so here's
    # one that looks nice.
    header = {'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.9; rv:32.0) Gecko/20100101 Firefox/32.0',}

    try:
        page = requests.get(url)
        return BeautifulSoup(page.text, 'html.parser')
    except Exception as e:
        print(e)
        return None

def soup_to_citation(url, soup):
    df = Datafinder(soup)

    citation = Citation()
    citation.authors = df.get_authors()
    citation.title = df.get_title()
    citation.access_date = datetime.datetime.now()
    citation.publication_date = df.get_publication_date()
    citation.url = url
    return citation

def main():
    
    isURL = False
    url = ''
    formatter = PolicyFormatter()
    citations = []

    print('Enter a URL')
    url = input()    

    while not isURL:
        isURL = checkers.is_url(url)
        if isURL:
            break
        print('Enter a URL')
        url = input()
        
    soup = url_to_soup(url)
    if (isURL is not False):
        if (soup is not None):
            citations.append(soup_to_citation(url, soup))
        else:
            print("Unable to load " + str(url), file=sys.stderr)

    if (False and args.from_file is not False):
        with open(args.from_file) as f:
            for line in f:
                print(".", end="", file=sys.stderr)
                sys.stderr.flush()
                soup = url_to_soup(line)
                if (soup is not None):
                    citations.append(soup_to_citation(line, soup))
                else:
                    print("Unable to load " + str(args.url), file=sys.stderr)

    formatted_citations = []
    for citation in citations:
        formatted_citations.append(formatter.format(citation))

    formatted_citations.sort()
    if (False and args.to_text is not False):
        with open(args.to_text, "w") as f:
            for citation in formatted_citations:
                f.write(citation)
                f.write("\n\n")
    else:
        for citation in formatted_citations:
            print(citation)

if __name__ == "__main__":
    main()
