# coding=utf-8

import os
import sys

from workflow import web, Workflow


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


def get_currencies():
    return os.getenv("CURRENCIES", "").replace(" ", "").split(",")


def fetch_exchanges(currency, currencies):
    response = web.get("https://tw.rter.info/capi.php").json()
    key = "USD{}".format(currency)

    if key not in response:
        error("'{}' is not a valid currency".format(currency))

    usd = response[key]["Exrate"]

    return {
        cur: response["USD{}".format(cur)]["Exrate"] / usd
        for cur in currencies if "USD{}".format(cur) in response
    }


def main(workflow):
    amount, currency = get_parameters(workflow)
    currencies = get_currencies()
    exchanges = fetch_exchanges(currency, currencies)

    for cur in currencies:
        if cur == currency:
            continue

        if cur not in exchanges:
            workflow.add_item(
                title="'{}' is not a valid currency".format(cur),
                valid=False
            )
            continue

        ex = exchanges[cur]

        title = "{:0.2f} {}".format(amount * ex, cur)
        subtitle = "1 {} = {:0.4f} {}".format(currency, ex, cur)

        workflow.add_item(
            title=title,
            subtitle=subtitle,
            arg=title.split(" ")[0],
            copytext=title,
            icon="./img/flags/{}.png".format(cur.lower()),
            valid=True
        )


if __name__ == u"__main__":
    wf = Workflow()
    wf.run(main)
    wf.send_feedback()
    sys.exit()
