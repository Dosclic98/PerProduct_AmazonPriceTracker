#!/usr/bin/python3

import json
from src.model.amazonItem import AmazonItem, AmazonItemEncoder


class ItemRepo:

    storagePath = "./data/storage/"

    def __init__(self, repoFileName):
        self.repoFileName = repoFileName

    # TODO Method for cleaning old objects in the repository (objects updated more than one month ago)

    def load(self):
        savedItems = set()
        try:
            fp = open(self.storagePath + self.repoFileName + ".json", "r")
            dic = json.load(fp)
            fp.close()
        except (FileNotFoundError, ValueError):
            return savedItems

        for item in dic:
            savedItems.add(AmazonItem.jsonToObject(item))

        return savedItems

    def save(self, itemsSet):
        itemsList = sorted(list(itemsSet), key=AmazonItem.takeId)
        fp = open(self.storagePath + self.repoFileName + ".json", "w")
        fp.write(json.dumps(itemsList, indent=4, cls=AmazonItemEncoder))
        fp.close()
