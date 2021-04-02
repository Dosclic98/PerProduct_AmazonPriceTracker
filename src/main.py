#!/usr/bin/python3

from model.amazonItem import AmazonItem, AmazonItemEncoder
from comp.amazonScraper import AmazonScraper
import json

def main():
    scraper = AmazonScraper(None)
    foundItems = scraper.searchItems("ssd", debug=False)
    for item in foundItems:
        print(json.dumps(item, indent=4, cls=AmazonItemEncoder))


if __name__ == "__main__":
    main()