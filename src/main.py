#!/usr/bin/python3

from src.model.amazonItem import AmazonItem, AmazonItemEncoder
from src.comp.amazonScraper import AmazonScraper
import json
from src.comp.itemsRepository import ItemRepo
from src.comp.telegramSender import TeleBotSender, MessageBuilder

bot = None

def main():
    global bot
    bot = TeleBotSender("@OfferteStorage")

    scraper = AmazonScraper()
    foundItemsSet = scraper.searchItemsMultiple(["ssd"])
    repoFileName = "testData"
    repo = ItemRepo(repoFileName)
    repoItemsSet = repo.load()
    print(len(foundItemsSet))
    itemsToStore = updateRepo(repoItemsSet, foundItemsSet)
    #repo.save(itemsToStore)

def updateRepo(savedItems, retrievedItems):
    global bot
    setToStore = set()
    savedItemsMap = buildItemsMap(savedItems)
    for item in retrievedItems:
        # 1) Retrieve the item if stored before
        try:
            storedItem = savedItemsMap[item.id]
        except KeyError:
            storedItem = None
        # 2.a) If no such item is present, then store the retrieved item and notify it through a message
        if(storedItem == None):
            bot.sendMessage(MessageBuilder.newItemFound(item))
            setToStore.add(item)
        else:
            if (( ((item.price != None and storedItem.price != None) and (item.price.amount_float < storedItem.price.amount_float)) or 
                    (item.price != None and storedItem.price == None)) and
                ( ((item.usedPrice != None and storedItem.usedPrice != None) and (item.usedPrice.amount_float < storedItem.usedPrice.amount_float)) or
                    (item.usedPrice != None and storedItem.usedPrice == None))):
                # TODO Bot new price and used price have gotten "better"
                print("Btr")
            elif ( ((item.price != None and storedItem.price != None) and (item.price.amount_float < storedItem.price.amount_float)) or 
                    (item.price != None and storedItem.price == None)):
                # TODO Only new peice has gotten better
                print("New Btr")
            elif ( ((item.usedPrice != None and storedItem.usedPrice != None) and (item.usedPrice.amount_float < storedItem.usedPrice.amount_float)) or
                    (item.usedPrice != None and storedItem.usedPrice == None)):
                # TODO only used price has goten better
                print("Used Btr")
            else:
                # TODO just store the result without having to notify
                print("Not Btr")
                
    return setToStore

def buildItemsMap(savedItems):
    itemsMap = {}
    for item in savedItems:
        itemsMap[item.id] = item

    return itemsMap

if __name__ == "__main__":
    main()