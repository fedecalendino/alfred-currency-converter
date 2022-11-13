from pycoingecko import CoinGeckoAPI

client = CoinGeckoAPI()


def get_rates(*ids):
    rates = []

    for coin in client.get_coins_markets("usd", ids=",".join(ids), per_page=10):
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


def search(symbol: str) -> list:
    symbol = symbol.lower()

    ids = []

    for coin in client.get_coins_list():
        if coin["symbol"] == symbol:
            ids.append(coin["id"])

    rates = get_rates(*ids)
    return rates[0] if rates else None
