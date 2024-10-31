import requests

BASE_URL = "https://api.coingecko.com/api/v3/"


def get(service: str, api_key: str, params: dict = None) -> dict:
    response = requests.get(
        url=f"{BASE_URL}/{service}",
        headers={
            "x-cg-demo-api-key": api_key,
        },
        params=params,
    )

    return response.json()


def get_rates(api_key: str, *ids):
    response = get(
        "coins/markets",
        api_key=api_key,
        params={
            "vs_currency": "usd",
            "ids": ",".join(ids),
            "per_page": 10,
        },
    )

    rates = []

    for coin in response:
        if not coin["current_price"]:
            continue

        if not coin["market_cap_rank"]:
            coin["market_cap_rank"] = -1

        rates.append(
            {
                "id": coin["id"],
                "symbol": coin["symbol"].upper(),
                "name": coin["name"],
                "img": coin["image"],
                "price": 1 / coin["current_price"],
                "type": "crypto",
            }
        )

    return rates


def search(api_key: str, symbol: str) -> list:
    response = get(
        "coins/list",
        api_key=api_key,
    )

    symbol = symbol.lower()

    ids = []

    for coin in response:
        if coin["symbol"] == symbol:
            ids.append(coin["id"])

    rates = get_rates(api_key, *ids)
    return rates[0] if rates else None
