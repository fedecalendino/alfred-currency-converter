from functools import lru_cache

import requests


@lru_cache
def get_blackmarket_usd() -> float:
    response = requests.get(
        "https://www.dolarsi.com/api/api.php?type=valoresprincipales"
    )

    for item in response.json():
        item = item["casa"]

        if item["nombre"] == "Dolar Blue":
            compra = float(item["compra"].replace(",", "."))
            venta = float(item["venta"].replace(",", "."))

            return (compra + venta) / 2

    return None
