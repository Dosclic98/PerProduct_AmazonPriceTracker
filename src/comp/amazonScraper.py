#!/usr/bin/python3

import json
from model.amazonItem import AmazonItem
import requests
import urllib.parse
from bs4 import BeautifulSoup
from price_parser import Price

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
        'Content-Type': 'text/html'}


    itemsJsonKey = "items"

    def __init__(self, itemsFileName):
        self.itemsFileName = itemsFileName
        self.itemsList = list()
        
        # Manage file not found exception
        if(itemsFileName != None):
            itemsFile = open(itemsFileName)
            jsonData = json.load(itemsFile)
            for item in jsonData["items"]:
                self.itemsList.append(AmazonItem.jsonToObject(item))

    def searchItems(self, queryStr):
        foundItems = list()
        complUrl = self.baseUrl + self.searchUrlPart + self.searchKey + urllib.parse.quote_plus(queryStr)
        r = requests.get(complUrl, headers=self.headers)
        soup = BeautifulSoup(r.content, features="html5lib")
        for div in soup.findAll("div", {"data-component-type":"s-search-result"}):
            foundItems.append(self.initItemFromDiv(div))
        return foundItems

    def initItemFromDiv(self, div):
        id = div["data-uuid"]
        imgLink = div.findAll("img")[0]["src"]
        linkTitle = div.findAll("a", {"class":"a-link-normal a-text-normal"})[0]
        objLink = self.baseUrlRedirect + linkTitle["href"]
        title = linkTitle.findAll("span", {"class":"a-size-base-plus a-color-base a-text-normal"})[0].get_text()
        starsCont = div.findAll("span", {"class":"a-icon-alt"})
        stars = self.parseStarStr(None 
                                    if len(starsCont) == 0 
                                    else div.findAll("span", {"class":"a-icon-alt"})[0].get_text())
        price = Price.fromstring(div.findAll("span", {"class":"a-offscreen"})[0].get_text())
        isPrime = False if len(div.findAll("i", {"class":"a-icon a-icon-prime a-icon-medium"})) == 0 else True
        # TODO Used price still to scrape


        # Debug Tests
        print("Id: " + id)
        print("ImgLink: " + imgLink)
        print("ObjLink: " + objLink)
        print("Title: " + title)
        print("RevStar: " + str(stars))
        print("Price: " + price.amount_text + " " + price.currency)
        print("IsPrime: " + str(isPrime))
        print(" ")

    def parseStarStr(self, strStar):
        return strStar



        