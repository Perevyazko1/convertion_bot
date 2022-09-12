import telebot

from config import keys, TOKEN
from exeptions import CryptoConvertion, APIException
import pymorphy2
morph = pymorphy2.MorphAnalyzer()

bot = telebot.TeleBot(TOKEN, parse_mode='HTML')


@bot.message_handler(commands=['start', 'help'])
def help(message: telebot.types.Message):
    user = message.chat.first_name
    text = f'Привет {user}! \n\n' \
           '<i>Чтобы узнать курс, введите сообщение в формате:</i>\n\n <u><b>доллар рубль 1</b></u> '
    bot.reply_to(message, text)


@bot.message_handler(commands=['values'])
def values(message: telebot.types.Message):
    text = '<i>Доступные валюты:</i>'
    for key in keys.keys():
        text = '\n'.join((text, key))
    bot.reply_to(message, text)


@bot.message_handler(content_types=['text'])
def convert(message: telebot.types.Message):
    try:
        values = message.text.split(' ')
        if len(values) != 3:
            raise APIException('Слишком много параметров!')
        quote, base, amount = values
        result = CryptoConvertion.get_price(quote, base, amount)
    except APIException as e:
        bot.reply_to(message, f'Ошибка пользователя \n {e}')
    except Exception as e:
        bot.reply_to(message, f'Не удалось конвертировать\n {e}')
    else:
        quote = morph.parse(quote)[0]
        base = morph.parse(base)[0]
        text = f'Цена за {amount} {quote.make_agree_with_number(int(amount)).word}: {result} - ' \
               f'{base.make_agree_with_number(int(amount)).word}'
        bot.send_message(message.chat.id, text)


bot.polling()
