#!/usr/bin/python3

import json
from model.amazonItem import AmazonItem
import requests
import urllib.parse
from bs4 import BeautifulSoup

class AmazonScraper:

    baseUrl = "https://www.amazon.it/"
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
        complUrl = self.baseUrl + self.searchUrlPart + self.searchKey + urllib.parse.quote_plus(queryStr)
        r = requests.get(complUrl, headers=self.headers)
        soup = BeautifulSoup(r.content, features="html5lib")
        #print(len(soup.findAll("div", {"data-component-type":"s-search-result"})))
        for div in soup.findAll("div", {"data-component-type":"s-search-result"}):
            print(div)


        