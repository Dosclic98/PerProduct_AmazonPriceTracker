#!/usr/bin/python3
import datetime
from json import JSONEncoder
from varname import nameof

class AmazonItem:

    def __init__(self, id, title = None, stars = None, objLink=None, imgLink = None, price = None, usedPrice = None, isPrime = None, ueDate = datetime.datetime.now()):
        self.id = id
        self.title = title
        self.stars = stars
        self.objLink = objLink
        self.imgLink = imgLink
        self.price = price
        self.usedPrice = usedPrice
        self.isPrime = isPrime
        self.ueDate = ueDate

    @staticmethod
    def jsonToObject(self, jsonDict):
        # TODO Converts json string to object
        return AmazonItem()
    
    def __str__(self):
        return AmazonItemKeys.id + " " + self.id + "\n" + AmazonItemKeys.imgLink + " " + self.imgLink + "\n" + AmazonItemKeys.objLink + " " + self.objLink + "\n" + AmazonItemKeys.title + " " + self.title + "\n" + AmazonItemKeys.stars + " " + str(self.stars) + "\n" + AmazonItemKeys.price + " " + str(self.price) + "\n" + AmazonItemKeys.usedPrice + " " + str(self.usedPrice) + "\n" + AmazonItemKeys.isPrime + " " + str(self.isPrime) + "\n"
    
class AmazonItemEncoder(JSONEncoder):

    def default(self, o):
        return {
                    AmazonItemKeys.id :o.id,
                    AmazonItemKeys.title : o.title,
                    AmazonItemKeys.stars : o.stars,
                    AmazonItemKeys.objLink :o.objLink,
                    AmazonItemKeys.imgLink :o.imgLink,
                    AmazonItemKeys.priceAmount : None if o.price == None else o.price.amount_float,
                    AmazonItemKeys.priceCurrency : None if o.price == None else o.price.currency,
                    AmazonItemKeys.usedPriceAmount : None if o.usedPrice == None else o.usedPrice.amount_float,
                    AmazonItemKeys.usedPriceCurrency : None if o.usedPrice == None else o.usedPrice.currency,
                    AmazonItemKeys.isPrime :o.isPrime,
                    AmazonItemKeys.ueDate :o.ueDate.isoformat(),
                }

class AmazonItemKeys:
    id = "id"
    title = "title"
    stars = "stars"
    objLink = "objLink"
    imgLink = "imgLink"
    priceAmount = "priceAmount"
    priceCurrency = "priceCurrency"
    usedPriceAmount = "usedPriceAmount"
    usedPriceCurrency = "usedPriceCurrency"
    isPrime = "isPrime"
    ueDate = "ueDate"