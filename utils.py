import requests
import json
from exeptions import keys



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
