#!/usr/bin/python3

import unittest
from src.model.amazonItem import AmazonItem, AmazonItemEncoder
from src.comp.amazonScraper import AmazonScraper
import json
from src.comp.itemsRepository import ItemRepo
from src.comp.telegramSender import TeleBotSender, MessageBuilder

class UnitTesting(unittest.TestCase):

    def testSerializeDeserialize(self):
        scraper = AmazonScraper()
        foundItemsSet = scraper.searchItems("ssd hard disk", debug=False)
        
        repo = ItemRepo("testData")
        repo.save(foundItemsSet)
        repoSet = repo.load()

        foundItems = sorted(list(foundItemsSet), key=lambda x: x.id, reverse=True)
        storedItems = sorted(list(repoSet), key=lambda x: x.id, reverse=True)
        self.assertEqual(len(foundItems), len(storedItems))
        for i in range(len(foundItems)):
            self.assertTrue(foundItems[i].identical(storedItems[i]))        
    
    def testMessages(self):
        firstItemDict = {
                            "id": "B07QJVNBKL",
                            "title": "ORICO Docking Station 5 bay USB 3.0 Tool-free Custodia per disco rigido magnetica 3.5\" per SATA External Hard Drive SATA3.0 da 5x10TB con adattatore 12V6.5A compatibile con Windows/Mac/Linux",
                            "stars": 4.2,
                            "objLink": "https://www.amazon.it/ORICO-Tool-free-magnetica-adattatore-compatibile/dp/B07QJVNBKL/ref=sr_1_60_sspa?dchild=1&keywords=ssd+hard+disk&qid=1618516908&sr=8-60-spons&psc=1&tag=dosclic98offe-21",
                            "imgLink": "https://m.media-amazon.com/images/I/51QlkWN-E5L._AC_UL320_.jpg",
                            "priceAmount": 160.2,
                            "priceCurrency": "\u20ac",
                            "usedPriceAmount": 137.99,
                            "usedPriceCurrency": "\u20ac",
                            "discount": None,
                            "isPrime": True,
                             "ueDate": "2021-04-15T22:01:46.837851"
                        }
        secondItemDict = {
                            "id": "B07QJVNBKL",
                            "title": "ORICO Docking Station 5 bay USB 3.0 Tool-free Custodia per disco rigido magnetica 3.5\" per SATA External Hard Drive SATA3.0 da 5x10TB con adattatore 12V6.5A compatibile con Windows/Mac/Linux",
                            "stars": 4.2,
                            "objLink": "https://www.amazon.it/ORICO-Tool-free-magnetica-adattatore-compatibile/dp/B07QJVNBKL/ref=sr_1_60_sspa?dchild=1&keywords=ssd+hard+disk&qid=1618516908&sr=8-60-spons&psc=1&tag=dosclic98offe-21",
                            "imgLink": "https://m.media-amazon.com/images/I/51QlkWN-E5L._AC_UL320_.jpg",
                            "priceAmount": 140.5,
                            "priceCurrency": "\u20ac",
                            "usedPriceAmount": 136.99,
                            "usedPriceCurrency": "\u20ac",
                            "discount": None,
                            "isPrime": True,
                             "ueDate": "2021-04-15T22:01:46.837851"
                        }
        thirdItemDict = {
                            "id": "B07QJVNBKL",
                            "title": "ORICO Docking Station 5 bay USB 3.0 Tool-free Custodia per disco rigido magnetica 3.5\" per SATA External Hard Drive SATA3.0 da 5x10TB con adattatore 12V6.5A compatibile con Windows/Mac/Linux",
                            "stars": 4.2,
                            "objLink": "https://www.amazon.it/ORICO-Tool-free-magnetica-adattatore-compatibile/dp/B07QJVNBKL/ref=sr_1_60_sspa?dchild=1&keywords=ssd+hard+disk&qid=1618516908&sr=8-60-spons&psc=1&tag=dosclic98offe-21",
                            "imgLink": "https://m.media-amazon.com/images/I/51QlkWN-E5L._AC_UL320_.jpg",
                            "priceAmount": 140.5,
                            "priceCurrency": "\u20ac",
                            "usedPriceAmount": 136.99,
                            "usedPriceCurrency": "\u20ac",
                            "discount": 10,
                            "isPrime": True,
                             "ueDate": "2021-04-15T22:01:46.837851"
                        }                        
        firstItem = AmazonItem.jsonToObject(firstItemDict)
        secondItem = AmazonItem.jsonToObject(secondItemDict)
        thirdItem = AmazonItem.jsonToObject(thirdItemDict)
        bot = TeleBotSender("@OfferteStorage")
        bot.sendMessage(MessageBuilder.newItemFound(obj=thirdItem))
        bot.sendMessage(MessageBuilder.newDiscountFound(obj=thirdItem))
        bot.sendMessage(MessageBuilder.betterPriceFound(stored=firstItem, obj=secondItem))

if __name__ == "__main__":
    unittest.main()