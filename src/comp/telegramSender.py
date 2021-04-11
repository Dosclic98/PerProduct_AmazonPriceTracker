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
        dic = json.load(open(self.botInfoPath + "botApiKey.json"))
        self.key = dic["key"]
        self.chat_id = dic[chatIdKey]
        self.bot = Bot(self.key)
    
    @sleep_and_retry
    @limits(calls=23, period=60)
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
    moneyEmoji = "\U0001f4b0"
    deliveryEmoji = "\U0001f69a"

    @staticmethod
    def newItemFound(obj):
        baseStr = MessageBuilder.redDotEmoji + " <b>Nuovo prodotto trovato!</b>\n\n"
        if(obj.title != None):
            baseStr += "<b>" + obj.title + "</b>" + "\n\n"
        priceStr = MessageBuilder.moneyEmoji + "  Prezzo nuovo:  {}\n"
        usedPriceStr = MessageBuilder.moneyEmoji + "  Prezzo usato:   {}\n"
        if(obj.price != None and obj.price.amount_float != None and obj.price.currency != None):
            baseStr += priceStr.format(str(obj.price.amount_float) + " " + str(obj.price.currency))
        if(obj.usedPrice != None and obj.usedPrice.amount_float != None and obj.usedPrice.currency != None):
            baseStr += usedPriceStr.format(str(obj.usedPrice.amount_float) + " " + str(obj.usedPrice.currency))

        starsStr = MessageBuilder.starEmoji + "  {}"+ " / 5" +"\n"
        if(obj.stars != None):
            baseStr += starsStr.format(str(obj.stars))
        
        if(obj.isPrime):
            baseStr += MessageBuilder.deliveryEmoji + "  Spedizione Prime"

        if(obj.imgLink != None):
            baseStr += '<a href="'+ obj.imgLink +'">&#8205;</a>'


        
        return (baseStr, obj.objLink)