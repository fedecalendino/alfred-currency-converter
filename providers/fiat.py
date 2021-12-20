from workflow import web

URL = "https://tw.rter.info/capi.php"


def fetch(currencies):
    currencies = set(map(lambda string: string.upper(), currencies))

    response = web.get(URL)
    data = response.json()

    exchanges = {}

    for currency in currencies:
        key = "USD{}".format(currency)

        if key not in data:
            exchanges[currency] = None
        else:
            exchanges[currency] = data[key]["Exrate"]

    return exchanges
