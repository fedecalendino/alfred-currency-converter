# coding=utf-8

import os
import sys

import providers
from workflow import Workflow


def error(title, subtitle=None):
    if subtitle:
        title = "{}: {}".format(title, subtitle)

    raise Exception(title)


def parse_amount(amount):
    amount = amount.upper().replace(',', '.')

    if amount.endswith("M"):
        mod = 1000000
        amount = amount[:-1]
    elif amount.endswith("K"):
        mod = 1000
        amount = amount[:-1]
    else:
        mod = 1

    return float(amount) * mod


def get_parameters(workflow):
    if len(workflow.args) != 2:
        error("Missing parameters", "$[amount] [currency]")

    try:
        amount = parse_amount(workflow.args[0])
        currency = workflow.args[1].strip().upper()

        return amount, currency
    except:
        error("'{}' is not a valid amount".format(workflow.args[0]))


def getenv(key):
    return os.getenv(key, "").replace(" ", "").split(",")


def fetch_exchanges(currency):
    cryptos = [currency] + getenv("CRYPTO")
    fiats = [currency] + getenv("FIAT")

    exchanges = {}

    for cur, ex in providers.crypto(cryptos).items():
        if cur in exchanges:
            continue

        if not ex:
            continue

        exchanges[cur] = {
            "type": "crypto",
            "exchange": ex,
        }

    for cur, ex in providers.fiat(fiats).items():
        if cur in exchanges:
            continue

        if not ex:
            continue

        exchanges[cur] = {
            "type": "fiat",
            "exchange": ex,
        }

    return exchanges


def main(workflow):
    amount, currency = get_parameters(workflow)
    currency = currency.upper()

    exchanges = fetch_exchanges(currency)

    if currency not in exchanges:
        raise ValueError("'{}' is not a valid currency".format(currency))

    exchange = exchanges[currency]["exchange"]

    for cur, info in exchanges.items():
        if cur == currency:
            continue

        if info is None:
            workflow.add_item(
                title="'{}' is not a valid currency".format(cur),
                valid=False
            )
            continue

        type_ = info["type"]
        ex = info["exchange"]

        title = "{:0.2f} {}".format(amount * ex / exchange, cur)
        subtitle = "1 {} = {:0.4f} {}".format(currency, ex / exchange, cur)

        workflow.add_item(
            title=title,
            subtitle=subtitle,
            arg=title.split(" ")[0],
            copytext=title,
            icon="./img/{}/{}.png".format(type_, cur).lower(),
            valid=True,
        )


if __name__ == u"__main__":
    wf = Workflow()
    wf.run(main)
    wf.send_feedback()
    sys.exit()
