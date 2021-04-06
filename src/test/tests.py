#!/usr/bin/python3

import unittest
from src.model.amazonItem import AmazonItem, AmazonItemEncoder
from src.comp.amazonScraper import AmazonScraper
import json
from src.comp.itemsRepository import ItemRepo

class UnitTesting(unittest.TestCase):

    def testSerializeDeserialize(self):
        scraper = AmazonScraper()
        foundItemsSet = scraper.searchItems("ssd", debug=False)
        
        repo = ItemRepo("testData.json")
        repo.save(foundItemsSet)
        repoSet = repo.load()

        foundItems = sorted(list(foundItemsSet), key=lambda x: x.id, reverse=True)
        storedItems = sorted(list(repoSet), key=lambda x: x.id, reverse=True)
        self.assertEqual(len(foundItems), len(storedItems))
        for i in range(len(foundItems)):
            self.assertTrue(foundItems[i].identical(storedItems[i]))        

if __name__ == "__main__":
    unittest.main()