import telebot
import requests
import json
import lxml.html
from lxml import etree

TOKEN = "5463577812:AAEeYWZMkwYjRxf3Gm_cEsGZvYxG__ohMY0"
bot = telebot.TeleBot(TOKEN)

keys = {'Биткоин': 'BTC',
        'Эфириум': 'ETH',
        'Доллар': 'USD'}


@bot.message_handler(commands=['start', 'help'])
def help(message: telebot.types.Message):
    text = 'Чтобы начать работу нажмите старт или выберите команду в меню '
    bot.reply_to(message, text)


@bot.message_handler(commands=['task'])
def values(message: telebot.types.Message):
    text = 'Доступные валюты:'
    for key in keys.keys():
        text = '\n'.join((text,key))
    bot.reply_to(message, text)





bot.polling(none_stop=True)
