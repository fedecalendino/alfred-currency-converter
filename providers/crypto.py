import os

from workflow import web

URL = "https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest"


def fetch(currencies):
    api_key = os.getenv("COINMARKETCAP_APIKEY")

    if not api_key:
        return {}

    currencies = set(map(lambda string: string.upper(), currencies))

    headers = {
        "Accept": "application/json",
        "X-CMC_PRO_API_KEY": api_key,
    }

    params = {
        "convert": "USD",
        "skip_invalid": "true",
        "symbol": ",".join(currencies),
    }

    response = web.get(URL, headers=headers, params=params)
    data = response.json()["data"]

    exchanges = {}

    for currency in currencies:
        if currency not in data:
            exchanges[currency] = None
        else:
            exchanges[currency] = 1 / data[currency]["quote"]["USD"]["price"]

    return exchanges
