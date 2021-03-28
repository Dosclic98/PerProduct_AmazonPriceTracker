#!/usr/bin/python3

from model.amazonItem import AmazonItem
from comp.amazonScraper import AmazonScraper
import json

def main():
    scraper = AmazonScraper(None)
    scraper.searchItems("ssd")


if __name__ == "__main__":
    main()