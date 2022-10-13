def get_env_list(workflow, key):
    return list(map(str.strip, workflow.env.get(key, "").split("\n")))


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
