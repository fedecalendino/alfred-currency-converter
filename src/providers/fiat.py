import requests

URL = "https://tw.rter.info/capi.php"


def fetch(currencies):
    currencies = set(map(lambda string: string.upper(), currencies))

    response = requests.get(URL)
    data = response.json()

    exchanges = {}

    for currency in currencies:
        key = "USD{}".format(currency)

        if key not in data:
            exchanges[currency] = None
        else:
            exchanges[currency] = {
                "currency": currency,
                "img": "./img/fiat/{}.png".format(currency).lower(),
                "exchange": data[key]["Exrate"],
                "type": "fiat",
            }

    return exchanges
