#!/usr/bin/python3

from src.model.amazonItem import AmazonItem, AmazonItemEncoder
from src.comp.amazonScraper import AmazonScraper
import json
from src.comp.itemsRepository import ItemRepo

def main():
    scraper = AmazonScraper()
    foundItemsSet = scraper.searchItems("ssd", debug=False)
    
    repo = ItemRepo("testData.json")
    repo.save(foundItemsSet)
    repoSet = repo.load()
    for item in repoSet:
        print(item)
    print(len(repoSet))

if __name__ == "__main__":
    main()