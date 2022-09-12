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


class ConvertionExeptions(Exception):
    pass


class CryptoConvertion:
    @staticmethod
    def convert(quote: str, base: str, amount: str):


        if quote == base:
            raise ConvertionExeptions('Вы указади одинаковые валюты!')
        try:
            quote_ticker = keys[quote]
        except KeyError:
            raise ConvertionExeptions(f'Не удалось обработать валюту {quote}')

        try:
            base_ticker = keys[base]
        except KeyError:
            raise ConvertionExeptions(f'Не удалось обработать валюту {base}')

        try:
            amount == float(amount)
        except ValueError:
            raise ConvertionExeptions(f'Не удалось обработать количество {amount}')

        r = requests.get(f'https://min-api.cryptocompare.com/data/price?fsym={quote_ticker}&tsyms={base_ticker}')
        total_base = json.loads(r.content)[keys[base]]

        return total_base

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
    values = message.text.split(' ')
    if len(values) != 3:
        raise ConvertionExeptions('Слишком много параметров!')
    quote, base, amount = values
    total_base = CryptoConvertion.convert(quote,base,amount)
    text = f'Цена {amount} {quote} в {base} - {total_base}'
    bot.send_message(message.chat.id ,text)


bot.polling()
