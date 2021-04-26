#!/usr/bin/python3

from src.model.amazonItem import AmazonItem, AmazonItemEncoder
from src.comp.amazonScraper import AmazonScraper
from src.comp.itemsRepository import ItemRepo
from src.comp.telegramSender import TeleBotSender, MessageBuilder
from src.keepAlive import keep_alive
import json
import argparse
import time
import sys, traceback, os


bot = None

# TODO Add a Daemon mode where the program is executed continuously every specified delay
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-repo", "-r", dest="repo", nargs=1, type=str, help="name of the file where the products will be stored (no .json extension needed)", required=True)
    parser.add_argument("-channel", "-c", dest="channel", nargs=1, type=str, help="name of the channel where the bot must send the generated messages (usually formatted as @channelName)", required=True)
    parser.add_argument("-queries", "-q", dest="queries", nargs="+", type=str, help="various queries (list of keywords) that the bot must monitor", required=True)
    parser.add_argument("--init", dest="initlz", action="store_true", help="use this parameter to specify if you want to initialize the reposotory doing 5 sequential run of the algorithm")
    parser.add_argument("--debug", dest="debug", action="store_true", help="print additional informations for debug purposes")
    parser.add_argument("--daemon", dest="daemon", action="store_true", help="start the program in daemon mode, where the price checking will be executed every, at most, 'delay' seconds (if not specified the delay will be 60 seconds)")
    parser.add_argument("-delay", dest="delay", nargs=1, type=int, help="delay used when de daemon parameter is specified")
    parser.set_defaults(initlz=False)
    parser.set_defaults(debug=False)
    parser.set_defaults(daemon=False)
    args = parser.parse_args()
    repoFileName = args.repo[0]
    queries = args.queries
    channelName = args.channel[0]
    delay = args.delay[0] if args.delay else 60
    print(queries)
    keep_alive()

    if args.initlz:
        for i in range(5):
            botLoop(channelName, repoFileName, queries, args.debug)
    elif args.daemon:
        while True:
            botLoop(channelName, repoFileName, queries, args.debug)
            try:
                time.sleep(delay)
            except KeyboardInterrupt:
                print("Interrupted")
                try:
                    sys.exit(0)
                except SystemExit:
                    os._exit(0)                
    else:
        botLoop(channelName, repoFileName, queries, args.debug)

def botLoop(channelName, repoFileName, queries, debug=False):
    global bot
    if bot == None:
        bot = TeleBotSender(channelName)
    print("** Starting loop execution **")
    scraper = AmazonScraper()
    print("Searching for updates...")
    foundItemsSet = scraper.searchItemsMultipleQuery(queries, debug=debug)
    print("   Found: " + str(len(foundItemsSet)) + (" item" if len(foundItemsSet) == 1 else " items"))
    repo = ItemRepo(repoFileName)
    print("Retrieving stored items...")
    repoItemsSet = repo.load()
    print("   Found: " + str(len(repoItemsSet)) + (" item" if len(repoItemsSet) == 1 else " items"))
    print("Sending messages...")
    itemsToStore = updateRepo(repoItemsSet, foundItemsSet)
    repo.save(itemsToStore) 
    print("Storing results...")
    print("** Ending loop execution **")

def updateRepo(savedItems, retrievedItems):
    global bot
    setToStore = set()
    savedItemsMap = buildItemsMap(savedItems)
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
                    (item.price != None and storedItem.price == None)) ):
                # New price has gotten "better" (used price notification removed due to Amazon used price showing policy)
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