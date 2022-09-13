import requests
import json
from config import keys


class APIException(Exception):
    pass


class CryptoConvertion:
    @staticmethod
    def get_price(quote: str, base: str, amount: str):

        if quote == base:
            raise APIException('Вы указали одинаковые валюты!')
        try:
            quote_ticker = keys[str.lower(quote)]
        except KeyError:
            raise APIException(f'Не удалось обработать валюту {quote}')

        try:
            base_ticker = keys[str.lower(base)]
        except KeyError:
            raise APIException(f'Не удалось обработать валюту {base}')

        try:
            amount == float(amount)
        except ValueError:
            raise APIException(f'Не удалось обработать количество {amount}')

        url = f"https://api.apilayer.com/fixer/convert?to={base_ticker}&from={quote_ticker}&amount={amount}"

        payload = {}
        headers = {
            "apikey": "FTsSQG8T440ithB5vdeu1ZacbSI3m62C"
        }

        response = requests.request("GET", url, headers=headers, data=payload)

        result = round(json.loads(response.text)['result'], 2)
        return result
