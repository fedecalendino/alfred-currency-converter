import sys

from pyflow.item import Item
from pyflow.workflow import Workflow

import environment
import api
import util


def fetch_rates(workflow: Workflow):
    rates = {}

    fiats = util.get_env_list(workflow, environment.FIAT)
    for info in api.fiat.get_rates(*fiats):
        rates[info["symbol"]] = info

    api_key = workflow.env.get(environment.COINGECKO_API_KEY)

    if api_key:
        cryptos = util.get_env_list(workflow, environment.CRYPTO)

        for info in api.crypto.get_rates(api_key, *cryptos):
            rates[info["symbol"]] = info

    return rates


def fetch_rate(workflow: Workflow, currency: str):
    if api.fiat.is_fiat(currency):
        return api.fiat.get_rates(currency)[0]

    api_key = workflow.env.get(environment.COINGECKO_API_KEY)

    if api_key:
        return api.crypto.search(api_key, currency)

    return None


def get_parameters(workflow: Workflow):
    if len(workflow.args) != 2:
        raise ValueError("Missing parameters: $[amount] [currency]")

    amount = workflow.args[0]

    try:
        amount = util.parse_amount(workflow.args[0])
    except ValueError:
        raise ValueError(f"'{amount}' is not a valid amount")

    currency = workflow.args[1].strip().upper()

    return amount, currency


def add_image_to_item(item: Item, img: str, id_: str):
    if "http" in img:
        item.set_icon_url(url=img, filename=f"{id_}.png")
    else:
        item.set_icon_file(path=img)


def main(workflow: Workflow):
    input_amount, input_currency = get_parameters(workflow)
    input_info = fetch_rate(workflow, input_currency)

    if input_info is None:
        raise ValueError("'{}' is not a valid currency".format(input_currency))

    input_price = input_info["price"]

    item = workflow.new_item(
        title=input_info["name"],
        subtitle=input_info["symbol"] + " / " + input_info["type"],
        valid=False,
    )

    add_image_to_item(item, input_info["img"], input_info["id"])

    for key, info in fetch_rates(workflow).items():
        if info["symbol"] == input_currency:
            continue

        if info is None:
            workflow.new_item(
                title=f"'{key}' is not a valid currency",
                valid=False,
            )
            continue

        ex = info["price"]
        total = input_amount * ex / input_price

        if total < 1:
            title = f"{total:,.6f} {info['symbol']}"
        else:
            title = f"{total:,.2f} {info['symbol']}"

        subtitle = "[{}] 1 {} = {:,.4f} {}".format(
            info["type"],
            input_currency,
            ex / input_price,
            info["symbol"],
        )

        item = workflow.new_item(
            title=title,
            subtitle=subtitle,
            arg=title.split(" ")[0].replace(",", ""),
            copytext=title,
            valid=True,
        )

        add_image_to_item(item, info["img"], info["id"])


if __name__ == "__main__":
    wf = Workflow()
    wf.run(main)
    wf.send_feedback()
    sys.exit()
