#!/usr/bin/python3

import unittest
from src.model.amazonItem import AmazonItem, AmazonItemEncoder
from src.comp.amazonScraper import AmazonScraper
import json

class UnitTesting(unittest.TestCase):

    def testSerializeDeserialize(self):
        scraper = AmazonScraper()
        foundItemsSet = scraper.searchItems("ssd", debug=False)
        foundItems = list(foundItemsSet)
        fp = open("testData.json", "w")
        fp.write(json.dumps(foundItems, indent=4, cls=AmazonItemEncoder))
        fp.close()

        fp = open("testData.json", "r")
        dic = json.load(fp)

        for i in range(len(foundItems)):
            #print("Printing object " + str(i+1))
            #print(foundItems[i])
            #print(AmazonItem.jsonToObject(jsonDict=dic[i]))
            #print("*************************************")
            self.assertTrue(foundItems[i] == AmazonItem.jsonToObject(jsonDict=dic[i]))

if __name__ == "__main__":
    unittest.main()