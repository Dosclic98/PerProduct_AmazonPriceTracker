#!/usr/bin/python3

class AmazonItem:

    def __init__(self, id, title = None, stars = None, imgLink = None, price = None, usedPrice = None, isPrime = None):
        self.id = id
        self.title = title
        self.stars = stars
        self.imgLink = imgLink
        self.price = price
        self.usedPrice = usedPrice
        self.isPrime = isPrime

    @staticmethod
    def jsonToObject(self, jsonStr):
        # Converts json string to object
        return AmazonItem()