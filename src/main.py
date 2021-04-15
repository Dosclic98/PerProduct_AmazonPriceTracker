#!/usr/bin/python3

from src.model.amazonItem import AmazonItem, AmazonItemEncoder
from src.comp.amazonScraper import AmazonScraper
import json
from src.comp.itemsRepository import ItemRepo
from src.comp.telegramSender import TeleBotSender, MessageBuilder

bot = None

def main():
    # TODO Introduction of parameter system for command line execution
    # TODO Add method to initialize repository doing 5 sequential execution of the program (to completely fill the repository) 
    global bot
    bot = TeleBotSender("@OfferteStorage")

    scraper = AmazonScraper()
    foundItemsSet = scraper.searchItems("ssd hard disk")
    repoFileName = "lolData"
    repo = ItemRepo(repoFileName)
    repoItemsSet = repo.load()
    print(len(foundItemsSet))
    itemsToStore = updateRepo(repoItemsSet, foundItemsSet)
    repo.save(itemsToStore)

def updateRepo(savedItems, retrievedItems):
    global bot
    setToStore = set()
    savedItemsMap = buildItemsMap(savedItems)
    print(len(savedItemsMap))
    for item in retrievedItems:
        # 1) Retrieve the item if stored before
        storedItem = None
        try:
            storedItem = savedItemsMap[item.id]
        except KeyError:
            storedItem = None
            assert(not savedItems.__contains__(item))
        # 2.a) If no such item is present, then store the retrieved item and notify it through a message
        if(storedItem == None):
            bot.sendMessage(MessageBuilder.newItemFound(item))
        else:
            if item.discount != None and ((storedItem.discount == None) or (storedItem.discount != None and item.discount > storedItem.discount)):
                # Found a new discount
                bot.sendMessage(MessageBuilder.newDiscountFound(item))
            elif (( ((item.price != None and storedItem.price != None) and (item.price.amount_float < storedItem.price.amount_float)) or 
                    (item.price != None and storedItem.price == None)) and
                ( ((item.usedPrice != None and storedItem.usedPrice != None) and (item.usedPrice.amount_float < storedItem.usedPrice.amount_float)) or
                    (item.usedPrice != None and storedItem.usedPrice == None))):
                # Bot new price and used price have gotten "better"
                bot.sendMessage(MessageBuilder.betterPriceFound(stored=storedItem, obj=item))
            elif ( ((item.price != None and storedItem.price != None) and (item.price.amount_float < storedItem.price.amount_float)) or 
                    (item.price != None and storedItem.price == None)):
                # TODO Only new peice has gotten better
                pass
            elif ( ((item.usedPrice != None and storedItem.usedPrice != None) and (item.usedPrice.amount_float < storedItem.usedPrice.amount_float)) or
                    (item.usedPrice != None and storedItem.usedPrice == None)):
                # TODO only used price has goten better
                pass
            else:
                # Just store the result without having to notify
                pass
        setToStore.add(item)
    for stItem in savedItems:
        if not setToStore.__contains__(stItem):
            setToStore.add(stItem)
            
    return setToStore

def buildItemsMap(savedItems):
    itemsMap = {}
    for item in savedItems:
        itemsMap[item.id] = item

    return itemsMap

if __name__ == "__main__":
    main()