#!/usr/bin/python3

from src.model.amazonItem import AmazonItem, AmazonItemEncoder
from src.comp.amazonScraper import AmazonScraper
from src.comp.itemsRepository import ItemRepo
from src.comp.telegramSender import TeleBotSender, MessageBuilder
import json
import argparse

bot = None

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-repo", "-r", dest="repo", nargs=1, type=str, help="name of the file where the products will be stored (no .json extension needed)", required=True)
    parser.add_argument("-channel", "-c", dest="channel", nargs=1, type=str, help="name of the channel where the bot must send the generated messages (usually formatted as @channelName)", required=True)
    parser.add_argument("-queries", "-q", dest="queries", nargs="+", type=str, help="various queries (list of keywords) that the bot must monitor", required=True)
    parser.add_argument("--init", dest="initlz", action="store_true", help="use this parameter to specify if you want to initialize the reposotory doing 5 sequential run of the algorithm")
    parser.add_argument("--debug", dest="debug", action="store_true", help="print additional informations for debug purposes")
    parser.set_defaults(initlz=False)
    parser.set_defaults(debug=False)
    args = parser.parse_args()
    repoFileName = args.repo[0]
    queries = args.queries
    channelName = args.channel[0]
    
    if args.initlz:
        for i in ragne(5):
            botLoop(channelName, repoFileName, queries, args.debug)
    else:
        botLoop(channelName, repoFileName, queries, args.debug)

def botLoop(channelName, repoFileName, queries, debug=False):
    global bot
    if bot == None:
        bot = TeleBotSender(channelName)

    scraper = AmazonScraper()
    foundItemsSet = scraper.searchItemsMultipleQuery(queries, debug=debug)
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
                    (item.price != None and storedItem.price == None)) or
                ( ((item.usedPrice != None and storedItem.usedPrice != None) and (item.usedPrice.amount_float < storedItem.usedPrice.amount_float)) or
                    (item.usedPrice != None and storedItem.usedPrice == None))):
                # New price or used price have gotten "better"
                bot.sendMessage(MessageBuilder.betterPriceFound(stored=storedItem, obj=item))
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