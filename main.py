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
    amount = amount.upper().replace(",", ".")

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

    for cur, info in providers.crypto(cryptos).items():
        if cur in exchanges:
            continue

        if not info:
            continue

        exchanges[cur] = info

    for cur, info in providers.fiat(fiats).items():
        if cur in exchanges:
            continue

        if not info:
            continue

        exchanges[cur] = info

    return exchanges


def main(workflow):
    selected_amount, selected_currency = get_parameters(workflow)
    selected_currency = selected_currency.upper()

    exchanges = fetch_exchanges(selected_currency)

    if selected_currency not in exchanges:
        raise ValueError("'{}' is not a valid currency".format(selected_currency))

    selected_exchange = exchanges[selected_currency]["exchange"]

    for cur in getenv("FIAT") + getenv("CRYPTO"):
        info = exchanges[cur]

        if cur == selected_currency:
            continue

        if info is None:
            workflow.add_item(
                title="'{}' is not a valid currency".format(cur),
                valid=False,
            )
            continue

        ex = info["exchange"]
        total = selected_amount * ex / selected_exchange

        if total < 1:
            title = "{:0.6f} {}".format(total, cur)
        else:
            title = "{:0.2f} {}".format(total, cur)

        subtitle = "[{}] 1 {} = {:0.4f} {}".format(
            info["type"],
            selected_currency,
            ex / selected_exchange,
            cur,
        )

        workflow.add_item(
            title=title,
            subtitle=subtitle,
            arg=title.split(" ")[0],
            copytext=title,
            icon=info["img"],
            valid=True,
        )


if __name__ == "__main__":
    wf = Workflow()
    wf.run(main)
    wf.send_feedback()
    sys.exit()
