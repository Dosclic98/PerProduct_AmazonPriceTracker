#!/usr/bin/python3

import json
from src.model.amazonItem import AmazonItem, AmazonItemEncoder


class ItemRepo:

    def __init__(self, repoFileName):
        self.repoFileName = repoFileName

    def load(self):
        try:
            fp = open(self.repoFileName, "r")
        except FileNotFoundError:
            return set()

        dic = json.load(fp)

        savedItems = set()
        for item in dic:
            savedItems.add(AmazonItem.jsonToObject(item))

        return savedItems

    def save(self, itemsSet):
        itemsList = list(itemsSet)
        fp = open(self.repoFileName, "w")
        fp.write(json.dumps(itemsList, indent=4, cls=AmazonItemEncoder))
        fp.close()
