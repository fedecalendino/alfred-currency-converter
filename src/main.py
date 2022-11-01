import sys

from pyflow import Workflow

import api
import util


def fetch_rates(workflow):
    rates = {}

    fiats = util.get_env_list(workflow, "FIAT")
    for info in api.fiat.get_rates(*fiats):
        rates[info["symbol"]] = info

    cryptos = util.get_env_list(workflow, "CRYPTO")
    for info in api.crypto.get_rates(*cryptos):
        rates[info["symbol"]] = info

    return rates


def fetch_rate(currency):
    if api.fiat.is_fiat(currency):
        return api.fiat.get_rates(currency)[0]

    return api.crypto.search(currency)


def get_parameters(workflow):
    if len(workflow.args) != 2:
        raise ValueError("Missing parameters: $[amount] [currency]")

    amount = workflow.args[0]

    try:
        amount = util.parse_amount(workflow.args[0])
    except ValueError:
        raise ValueError(f"'{amount}' is not a valid amount")

    currency = workflow.args[1].strip().upper()

    return amount, currency


def add_image_to_item(item, img: str, id_: str):
    if "http" in img:
        item.set_icon_url(url=img, filename=f"{id_}.png")
    else:
        item.set_icon_file(path=img)


def main(workflow):
    input_amount, input_currency = get_parameters(workflow)
    input_info = fetch_rate(input_currency)

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
            title = f"{total:0.6f} {info['symbol']}"
        else:
            title = f"{total:0.2f} {info['symbol']}"

        subtitle = "[{}] 1 {} = {:0.4f} {}".format(
            info["type"],
            input_currency,
            ex / input_price,
            info["symbol"],
        )

        mod_subtitle = None

        if key == "ARS":
            blackmarket_usd = api.ars.get_blackmarket_usd()
            blackmarket_total = input_amount * blackmarket_usd / input_price

            mod_subtitle = (
                f"🔵 {blackmarket_total:0.2f} {info['symbol']} (ARS blackmarket)"
            )
        elif input_currency == "ARS":
            blackmarket_usd = api.ars.get_blackmarket_usd()
            blackmarket_total = input_amount * ex / blackmarket_usd

            mod_subtitle = (
                f"🔵 {blackmarket_total:0.2f} {info['symbol']} (ARS blackmarket)"
            )

        item = workflow.new_item(
            title=title,
            subtitle=subtitle,
            arg=title.split(" ")[0],
            copytext=title,
            valid=True,
        )

        add_image_to_item(item, info["img"], info["id"])

        if mod_subtitle:
            item.set_cmd_mod(
                subtitle=mod_subtitle,
                arg=mod_subtitle.split(" ")[1],
            )

            item.set_alt_mod(
                subtitle=mod_subtitle,
                arg=mod_subtitle.split(" ")[1],
            )


if __name__ == "__main__":
    wf = Workflow()
    wf.run(main)
    wf.send_feedback()
    sys.exit()
