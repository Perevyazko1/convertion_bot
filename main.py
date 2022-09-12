import telebot

from config import keys, TOKEN
from exeptions import CryptoConvertion, APIException

bot = telebot.TeleBot(TOKEN, parse_mode='HTML')


@bot.message_handler(commands=['start', 'help'])
def help(message: telebot.types.Message):
    user = message.chat.first_name
    text = f'Привет {user}! \n\n' \
           '<i>Чтобы начать работу нажмите старт или выберите команду в меню</i> '
    bot.reply_to(message, text)


@bot.message_handler(commands=['values'])
def values(message: telebot.types.Message):
    text = 'Доступные валюты:'
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
        text = f'Цена за {amount} {quote} в {base} - {result}'
        bot.send_message(message.chat.id, text)


bot.polling()
