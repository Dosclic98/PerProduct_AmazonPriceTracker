#!/usr/bin/python3

import json
from src.model.amazonItem import AmazonItem
import requests
import urllib.parse
from bs4 import BeautifulSoup
from price_parser import Price
from decimal import Decimal

class AmazonScraper:

    baseUrlRedirect = "https://www.amazon.it"
    baseUrl = baseUrlRedirect + "/"
    searchUrlPart = "s?"
    searchKey = "k="    
    headers = {
            "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:66.0) Gecko/20100101 Firefox/66.0", 
            "Accept-Encoding":"gzip, deflate", 
            "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8", 
            "DNT":"1",
            "Connection":"close", 
            "Upgrade-Insecure-Requests":"1",
            "Content-Type": "text/html"
        }
    
    def searchItemsMultiple(self, queryStrList, debug = False):
        setToRet = set()
        for queryStr in queryStrList:
            foundItems = self.searchItems(queryStr, debug)
            setToRet = setToRet.union(foundItems)
        return setToRet

    def searchItems(self, queryStr, debug = False):
        foundItems = set()

        complUrl = self.baseUrl + self.searchUrlPart + self.searchKey + urllib.parse.quote_plus(queryStr)
        r = requests.get(complUrl, headers=self.headers)
        soup = BeautifulSoup(r.content, features="html5lib")
        
        for div in soup.findAll("div", {"data-component-type":"s-search-result"}):
            foundItems.add(self.initItemFromDiv(div, debug=debug))
        return foundItems

    def initItemFromDiv(self, div, debug=False):
        id = div["data-asin"]
        imgLink = div.findAll("img")[0]["src"]
        linkTitle = div.findAll("a", {"class":"a-link-normal a-text-normal"})[0]
        objLink = self.baseUrlRedirect + linkTitle["href"]
        title = linkTitle.findAll("span", {"class":"a-size-base-plus a-color-base a-text-normal"})[0].get_text()
        starsCont = div.findAll("span", {"class":"a-icon-alt"})
        stars = self.parseStarStr(None 
                                    if len(starsCont) == 0 
                                    else div.findAll("span", {"class":"a-icon-alt"})[0].get_text())
        priceVal = div.findAll("span", {"class":"a-price-whole"})
        priceSymbol = div.findAll("span", {"class":"a-price-symbol"})
        price = None if len(priceVal) == 0 or len(priceSymbol) == 0 else Price.fromstring(priceVal[0].get_text() + priceSymbol[0].get_text())

        usedPriceParent = div.findAll("div", {"class":"a-row a-size-base a-color-secondary"})
        if len(usedPriceParent) != 0:
            usedPriceCont = usedPriceParent[0].findAll("span", {"class":"a-color-base", "dir":"auto"})
            usedPrice = Price.fromstring(usedPriceCont[0].get_text()) if len(usedPriceCont) != 0 else None
        else:
            usedPrice = None

        isPrime = False if len(div.findAll("i", {"class":"a-icon a-icon-prime a-icon-medium"})) == 0 else True

        # Added for some edge cases where the used price gets read with "None" amount or currency
        if(usedPrice != None and (usedPrice.amount_float == None or usedPrice.currency == None)): usedPrice = None
        
        # Debug Tests
        if debug:
            print("Id: " + id)
            print("ImgLink: " + imgLink)
            print("ObjLink: " + objLink)
            print("Title: " + title)
            print("RevStar: " + str(stars))
            if(price != None):
                print("Price: " + price.amount_text + " " + price.currency)
            else:
                print("Price: Unknown")
            if(usedPrice != None):
                print("usedPrice: " + str(usedPrice.amount_text) + " " + str(usedPrice.currency))        
            print("IsPrime: " + str(isPrime))
            print(" ")
        
        return AmazonItem(id, title, stars, objLink, imgLink, price, usedPrice, isPrime)

    def parseStarStr(self, strStar):
        if strStar == None: return None
        else:
            starSplitted = strStar.split(sep=" ", maxsplit=1)
            return None if len(starSplitted) == 0 else float(starSplitted[0].replace(",", "."))



        