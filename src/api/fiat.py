import ccy
import requests


URL = "https://tw.rter.info/capi.php"

RATES = {
    key[3:]: value["Exrate"]
    for key, value in requests.get(URL).json().items()
    if key.startswith("USD") and key not in ["USDBTC"]
}


def is_fiat(currency):
    return ccy.currency(currency) is not None


def get_rates(*currencies):
    rates = []

    for currency in currencies:
        currency = ccy.currency(currency)

        if currency is None:
            continue

        rates.append(
            {
                "id": currency.code.lower(),
                "symbol": currency.code,
                "name": currency.name,
                "img": "./img/fiat/{}.png".format(currency.code),
                "price": RATES[currency.code.upper()],
                "type": "fiat",
            }
        )

    return rates
