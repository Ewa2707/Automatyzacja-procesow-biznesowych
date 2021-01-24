import re


def parse_price(price: str) -> float:
    try:
        price = re.search(r"[0-9.-]+,[0-9.-]+", price).group(0)
    except AttributeError:
        return None
    price = price.replace(',', '.')
    try:
        price = float(price)
    except (TypeError, ValueError):
        price = None
    finally:
        return price
