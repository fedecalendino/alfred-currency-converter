import os

import requests


BASE_URL = "https://pro-api.coinmarketcap.com/v1"
LISTING_URL = BASE_URL + "/cryptocurrency/listings/latest"
QUOTES_URL = BASE_URL + "/cryptocurrency/quotes/latest"

IMAGE_FILENAME = "/tmp/{id}.png"
IMAGE_URL = "https://s2.coinmarketcap.com/static/img/coins/128x128/{id}.png"


def fetch(currencies):
    api_key = os.getenv("COINMARKETCAP_API_KEY")

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

    response = requests.get(QUOTES_URL, headers=headers, params=params)
    data = response.json()["data"]

    exchanges = {}

    for currency in currencies:
        if currency not in data:
            exchanges[currency] = None
        else:
            exchanges[currency] = {
                "currency": currency,
                "img": get_image(data[currency]["id"]),
                "exchange": 1 / data[currency]["quote"]["USD"]["price"],
                "type": "crypto",
            }

    return exchanges


def load_image(id_):
    filename = IMAGE_FILENAME.format(id=id_)
    return filename if os.path.isfile(filename) else None


def get_image(id_):
    filename = load_image(id_)

    if filename:
        return filename

    filename = IMAGE_FILENAME.format(id=id_)

    url = IMAGE_URL.format(id=id_)

    with open(filename, "wb") as f:
        f.write(requests.get(url).content)

    return f.name
