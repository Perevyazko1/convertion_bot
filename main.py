import telebot
import requests
import json
import lxml.html
from lxml import etree

TOKEN = "5463577812:AAEeYWZMkwYjRxf3Gm_cEsGZvYxG__ohMY0"
bot = telebot.TeleBot(TOKEN)

keys = {'биткоин': 'BTC',
        'эфириум': 'ETH',
        'доллар': 'USD'}




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


@bot.message_handler(content_types=['text'])
def convert(message: telebot.types.Message):
    quote, base, amount = message.text.split(' ')
    r = requests.get(f'https://min-api.cryptocompare.com/data/price?fsym={keys[quote]}&tsyms={keys[base]}')
    total_loads = json.loads(r.content)[keys[base]]
    text = f'{amount} {quote} в {base} - {total_loads}'
    bot.send_message(message.chat.id ,text)


bot.polling(none_stop=True)
