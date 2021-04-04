#!/usr/bin/python3

from src.model.amazonItem import AmazonItem, AmazonItemEncoder
from src.comp.amazonScraper import AmazonScraper
import json

def main():
    scraper = AmazonScraper()
    foundItemsSet = scraper.searchItems("ssd", debug=False)
    foundItems = list(foundItemsSet)
    fp = open("testData.json", "w")
    fp.write(json.dumps(foundItems, indent=4, cls=AmazonItemEncoder))
    fp.close()

    fp = open("testData.json", "r")
    dic = json.load(fp)

    for i in range(5):
        print("Printing object " + str(i+1))
        print(foundItems[i])
        print(AmazonItem.jsonToObject(jsonDict=dic[i]))
        print(foundItems[i] == AmazonItem.jsonToObject(jsonDict=dic[i]))
        print("*************************************")


if __name__ == "__main__":
    main()