from telegram import Bot, ParseMode, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.error import RetryAfter
from telegram.error import TimedOut as TeleTimedOut
from telegram.ext import messagequeue as mq
from src.model.amazonItem import AmazonItem
from ratelimit import limits, sleep_and_retry
import json
import time

class TeleBotSender:

    botInfoPath = "./data/api/"
    sleepAfterTimeout = 5   #seconds
    maxSendFail = 5

    def __init__(self, chatIdKey):
        fp = open(self.botInfoPath + "botApiKey.json")
        dic = json.load(fp)
        fp.close()
        self.key = dic["key"]
        self.chat_id = dic[chatIdKey]
        self.bot = Bot(self.key)
    
    @sleep_and_retry
    @limits(calls=19, period=60)
    def sendMessage(self, pair):
        pinEmoji = "\U0001f4cc"
        failures = 0
        while failures < self.maxSendFail:
            try:            
                if(pair[1] != None):
                    keyboard = [[InlineKeyboardButton(pinEmoji + " Vai al prodotto", url=pair[1])]]
                    replyMarkup = InlineKeyboardMarkup(keyboard)
                    self.bot.send_message(chat_id = self.chat_id, text=pair[0], disable_web_page_preview=False, parse_mode=ParseMode.HTML, reply_markup=json.dumps(replyMarkup.to_dict()))
                else:
                    self.bot.send_message(chat_id = self.chat_id, text=pair[0], disable_web_page_preview=False, parse_mode=ParseMode.HTML)
                time.sleep(0.5)     # just to not get often TimedOut by Telegram so we don't get banned

            except RetryAfter as rtrExc:
                time.sleep(rtrExc.retry_after)
                failures += 1
            except TeleTimedOut:
                time.sleep(self.sleepAfterTimeout)
                failures += 1
            else:
                break

class MessageBuilder:
    
    starEmoji = "\U00002b50"
    redDotEmoji = "\U0001f534"
    greenDotEmoji = "\U0001f7e2"
    moneyEmoji = "\U0001f4b0"
    flyMoneyEmoji = "\U0001f4b8"
    deliveryEmoji = "\U0001f69a"

    @staticmethod
    def newItemFound(obj):
        baseStr = MessageBuilder.greenDotEmoji + " <b>Nuovo prodotto!</b>\n\n"
        if(obj.title != None):
            baseStr += "<b>" + obj.title + "</b>" + "\n\n"
        priceStr = "\n" + (MessageBuilder.flyMoneyEmoji if obj.discount != None else MessageBuilder.moneyEmoji) + " Prezzo nuovo:  {}"
        discStr = " con uno sconto del {}%"
        usedPriceStr = "\n" + MessageBuilder.moneyEmoji + " Prezzo usato:   {}"
        if(obj.price != None and obj.price.amount_float != None and obj.price.currency != None):
            if obj.discount != None:
                baseStr += (priceStr.format(str("%.2f" % (obj.price.amount_float - (obj.price.amount_float * (obj.discount/100)))) + " " + str(obj.price.currency)) + discStr.format(str(obj.discount)))
            else:
                baseStr += priceStr.format(str("%.2f" % obj.price.amount_float) + " " + str(obj.price.currency))
        if(obj.usedPrice != None and obj.usedPrice.amount_float != None and obj.usedPrice.currency != None):
            baseStr += usedPriceStr.format(str("%.2f" % obj.usedPrice.amount_float) + " " + str(obj.usedPrice.currency))

        starsStr = "\n" + MessageBuilder.starEmoji + "  {}"+ " / 5"
        if(obj.stars != None):
            baseStr += starsStr.format(str(obj.stars))
        
        if(obj.isPrime):
            baseStr += "\n" + MessageBuilder.deliveryEmoji + "  Spedizione Prime"

        if(obj.imgLink != None):
            baseStr += '<a href="'+ obj.imgLink +'">&#8205;</a>'
        
        return (baseStr, obj.objLink)

    @staticmethod
    def newDiscountFound(obj):
        baseStr = MessageBuilder.redDotEmoji + " <b>Nuovo sconto!</b>\n\n"
        if(obj.title != None):
            baseStr += "<b>" + obj.title + "</b>" + "\n\n"
        priceStr = "\n" + (MessageBuilder.flyMoneyEmoji if obj.discount != None else MessageBuilder.moneyEmoji) + " Prezzo nuovo:  {}"
        discStr = " con uno sconto del {}%"
        usedPriceStr = "\n" + MessageBuilder.moneyEmoji + " Prezzo usato:   {}"
        if(obj.price != None and obj.price.amount_float != None and obj.price.currency != None):
            if obj.discount != None:
                baseStr += (priceStr.format(str("%.2f" % (obj.price.amount_float - (obj.price.amount_float * (obj.discount/100)))) + " " + str(obj.price.currency)) + discStr.format(str(obj.discount)))
            else:
                baseStr += priceStr.format(str("%.2f" % obj.price.amount_float) + " " + str(obj.price.currency))
        if(obj.usedPrice != None and obj.usedPrice.amount_float != None and obj.usedPrice.currency != None):
            baseStr += usedPriceStr.format(str("%.2f" % obj.usedPrice.amount_float) + " " + str(obj.usedPrice.currency))

        starsStr = "\n" + MessageBuilder.starEmoji + "  {}"+ " / 5"
        if(obj.stars != None):
            baseStr += starsStr.format(str(obj.stars))
        
        if(obj.isPrime):
            baseStr += "\n" + MessageBuilder.deliveryEmoji + "  Spedizione Prime"

        if(obj.imgLink != None):
            baseStr += '<a href="'+ obj.imgLink +'">&#8205;</a>'

        return (baseStr, obj.objLink)

    @staticmethod
    def betterPriceFound(stored, obj):
        baseStr = MessageBuilder.redDotEmoji + " <b>Calo di prezzo!</b>\n\n"
        if(obj.title != None):
            baseStr += "<b>" + obj.title + "</b>" + "\n\n"
        priceStr = "\n" + (MessageBuilder.flyMoneyEmoji if obj.discount != None else MessageBuilder.moneyEmoji) + " Prezzo nuovo:  {}"
        discStr = " con uno sconto del {}%"
        usedPriceStr = "\n" + MessageBuilder.moneyEmoji + " Prezzo usato:   {}"
        if(stored.price != None and stored.price.amount_float != None and stored.price.currency != None and obj.price != None and obj.price.amount_float != None and obj.price.currency != None):
            if obj.discount != None:
                if stored.price.amount_float > obj.price.amount_float:
                    baseStr += (priceStr.format(str("%.2f" % (obj.price.amount_float - (obj.price.amount_float * (obj.discount/100)))) + " " + str(obj.price.currency)) + discStr.format(str(obj.discount)) + " invece di " + str("%.2f" % stored.price.amount_float) + " " + str(stored.price.currency))
                else:
                    baseStr += (priceStr.format(str("%.2f" % (obj.price.amount_float - (obj.price.amount_float * (obj.discount/100)))) + " " + str(obj.price.currency)) + discStr.format(str(obj.discount)))
            else:
                if stored.price.amount_float > obj.price.amount_float:
                    baseStr += priceStr.format(str("%.2f" % obj.price.amount_float) + " " + str(obj.price.currency) + " invece di " + str("%.2f" % stored.price.amount_float) + " " + str(stored.price.currency))
                else:
                    baseStr += priceStr.format(str("%.2f" % obj.price.amount_float) + " " + str(obj.price.currency))
        elif(stored.price == None and obj.price != None and obj.price.amount_float != None and obj.price.currency != None):
            if obj.discount != None:
                baseStr += (priceStr.format(str("%.2f" % (obj.price.amount_float - (obj.price.amount_float * (obj.discount/100)))) + " " + str(obj.price.currency)) + " appena aggiunto" + discStr.format(str(obj.discount)))
            else:
                baseStr += priceStr.format(str("%.2f" % obj.price.amount_float) + " " + str(obj.price.currency) + " appena aggiunto!")
        # If the used price has gotten better or a new used element has been added
        if(stored.usedPrice != None and stored.usedPrice.amount_float != None and stored.usedPrice.currency != None and obj.usedPrice != None and obj.usedPrice.amount_float != None and obj.usedPrice.currency != None):
            if stored.usedPrice.amount_float > obj.usedPrice.amount_float:
                baseStr += usedPriceStr.format(str("%.2f" % obj.usedPrice.amount_float) + " " + str(obj.usedPrice.currency) + " invece di " + str("%.2f" % stored.usedPrice.amount_float) + " " + str(stored.usedPrice.currency))
            else:
                baseStr += usedPriceStr.format(str("%.2f" % obj.usedPrice.amount_float) + " " + str(obj.usedPrice.currency))
        elif(stored.usedPrice == None and obj.usedPrice != None and obj.usedPrice.amount_float != None and obj.usedPrice.currency != None):
            baseStr += usedPriceStr.format(str("%.2f" % obj.usedPrice.amount_float) + " " + str(obj.usedPrice.currency) + " appena aggiunto!")

        starsStr = "\n" + MessageBuilder.starEmoji + "  {}"+ " / 5"
        if(obj.stars != None):
            baseStr += starsStr.format(str(obj.stars))
        
        if(obj.isPrime):
            baseStr += "\n" + MessageBuilder.deliveryEmoji + "  Spedizione Prime"

        if(obj.imgLink != None):
            baseStr += '<a href="'+ obj.imgLink +'">&#8205;</a>'

        return (baseStr, obj.objLink)        