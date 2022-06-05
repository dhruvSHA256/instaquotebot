#!/usr/bin/env python
from bs4 import BeautifulSoup
import re
import requests
import json
from config import TAGS


def geturl(tag: list, page=1):
    return f"https://www.goodreads.com/quotes/tag/{tag}?page={page}"


def getquote(tag, page=1):
    url = geturl(tag, page)
    page = requests.get(url)
    soup = BeautifulSoup(page.content, "html.parser")
    quotes_elem = soup.find_all("div", {"class": "quote mediumText"})
    quotes = {"children": []}

    def extract_quote(elem):
        quote_text = elem.find("div", {"class": "quoteText"}).get_text(
            "|", strip=True
        )
        quote_text = quote_text.split("|")[0]
        quote_text = re.sub("^“", "", quote_text)
        quote_text = re.sub("”\s?$", "", quote_text)

        if len(quote_text) > 90:
            return None

        author = elem.find("span", {"class": "authorOrTitle"}).get_text()
        author = author.strip()
        author = author.rstrip(",")

        tags = elem.find("div", {"class": "greyText smallText left"}).get_text(
            strip=True
        )
        tags = re.sub("^tags:", "", tags)
        tags = tags.split(",")

        quote = {
            "text": quote_text,
            "author": author,
            "tags": tags,
            "used": False,
        }
        return quote

    for elem in quotes_elem:
        quote = extract_quote(elem)
        if quote:
            quotes["children"].append(quote)

    return quotes


def main():
    quotes = {}
    for tag in TAGS:
        quotes[tag] = getquote(tag)

    with open("quotes.json", "w") as json_file:
        json.dump(quotes, json_file, indent=4, sort_keys=True)


main()
