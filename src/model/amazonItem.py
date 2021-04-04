#!/usr/bin/python3
import datetime
from json import JSONEncoder
from varname import nameof
from price_parser import Price

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
    def jsonToObject(jsonDict):
        # Converts json string to object
        price = None if jsonDict[AmazonItemKeys.priceAmount] == None or jsonDict[AmazonItemKeys.priceCurrency] == None else Price.fromstring(str(jsonDict[AmazonItemKeys.priceAmount]) + " " + jsonDict[AmazonItemKeys.priceCurrency]) 
        usedPrice = None if jsonDict[AmazonItemKeys.usedPriceAmount] == None or jsonDict[AmazonItemKeys.usedPriceCurrency] == None else Price.fromstring(str(jsonDict[AmazonItemKeys.usedPriceAmount]) + " " + jsonDict[AmazonItemKeys.usedPriceCurrency])
        return AmazonItem(jsonDict[AmazonItemKeys.id], jsonDict[AmazonItemKeys.title], jsonDict[AmazonItemKeys.stars], jsonDict[AmazonItemKeys.objLink], 
                            jsonDict[AmazonItemKeys.imgLink], price, usedPrice, jsonDict[AmazonItemKeys.isPrime], 
                            datetime.datetime.fromisoformat(jsonDict[AmazonItemKeys.ueDate]))
    
    def __str__(self):
        return AmazonItemKeys.id + ": " + self.id + "\n" + AmazonItemKeys.imgLink + ": " + self.imgLink + "\n" + AmazonItemKeys.objLink + ": " + self.objLink + "\n" + AmazonItemKeys.title + ": " + self.title + "\n" + AmazonItemKeys.stars + ": " + str(self.stars) + "\n" + AmazonItemKeys.price + ": " + str(self.price) + "\n" + AmazonItemKeys.usedPrice + ": " + str(self.usedPrice) + "\n" + AmazonItemKeys.isPrime + ": " + str(self.isPrime) + "\n" + AmazonItemKeys.ueDate + ": " + self.ueDate.isoformat() + "\n"
    
    def __eq__(self, other):
        if isinstance(other, AmazonItem):
            isPriceEqual = self.isPriceEq(self.price, other.price)
            isUsedPriceEqual = self.isPriceEq(self.usedPrice, other.usedPrice)
            return self.id == other.id and self.title == other.title and self.stars == other.stars and self.objLink == other.objLink and self.imgLink == other.imgLink and isPriceEqual and isUsedPriceEqual and self.isPrime == other.isPrime and self.ueDate.isoformat() == other.ueDate.isoformat()
        return False

    def __hash__(self):
        return hash(self.id)
    
    def isPriceEq(self, thisPrice, thatPrice):
        if(thisPrice is not None and thatPrice is not None):
            return thisPrice.amount_float == thatPrice.amount_float and thisPrice.currency == thatPrice.currency
        else:
            if(thisPrice is None and thatPrice is None): return True
            else: return False

    @staticmethod
    def isPriceEqStatic(thisPrice, thatPrice):
        if(thisPrice is not None and thatPrice is not None):
            return thisPrice.amount_float == thatPrice.amount_float and thisPrice.currency == thatPrice.currency
        else:
            if(thisPrice is None and thatPrice is None): return True
            else: return False    

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
    price = "price"
    priceAmount = "priceAmount"
    priceCurrency = "priceCurrency"
    usedPrice = "usedPrice"
    usedPriceAmount = "usedPriceAmount"
    usedPriceCurrency = "usedPriceCurrency"
    isPrime = "isPrime"
    ueDate = "ueDate"