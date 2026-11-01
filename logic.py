import json
from datetime import datetime
from datetime import date


def load_shops():
    try:
        with open("discount_second.json", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        print("Файл .json не найден рядом с bot.py")
        raise
    except json.JSONDecodeError as e:
        print(f"Ошибка в JSON: строка {e.lineno}, символ: {e.colno}")
        raise


def get_price(shop, today):
    if shop["type"] == "cycle":
        start = date.fromisoformat(shop["start"])
        days_passed = (today - start).days
        place = days_passed % len(shop["price"])
        return shop["price"][place]
    elif shop["type"] == "period":
        for period in shop["periods"]:
            if (today >= date.fromisoformat(period["from"])) and (today <= date.fromisoformat(period["to"])):
                return period["price"]
        return "expired"
    return None


def finds_promos(shops, today):
    result = []
    for shop in shops:
        if get_price(shop, today) == "Акция":
            result.append(shop["name"])
    return result


def find_no_limit_top(shops, today):
    result = []
    expired = []
    for shop in shops:
        if shop["group"] == "no_limit":
            price = get_price(shop, today)
            if isinstance(price, int):
                result.append([shop["name"], price, shop["unit"]])
            elif price == "expired":
                expired.append(shop["name"])
    result.sort(key=lambda pair: pair[1])
    return result, expired


def find_limit_top(shops, today):
    result = []
    expired = []
    for shop in shops:
        if shop["group"] == "limit":
            price = get_price(shop, today)
            if isinstance(price, int):
                if shop["better"] == 'lower':
                    if shop["max"] >= price:
                        result.append([shop["name"], price, shop["unit"]])
                else:
                    if shop["max"] <= price:
                        result.append([shop["name"], price, shop["unit"]])
            elif price == "expired":
                expired.append(shop["name"])
    return result, expired


def build_where_text():
    SHOPS = load_shops()
    today = date.today()
    promos = finds_promos(SHOPS, today)
    top_shops, expired_top = find_no_limit_top(SHOPS, today)
    other_shops, expired_other = find_limit_top(SHOPS, today)
    text = ""
    if len(promos) != 0:
        text += "🔥 Акции здесь: " + ", ".join(promos) + "\n\n"
    text += "🏆 Лучшие цена в секондах сегодня\n"
    for name, price, unit in top_shops:
        text += f"{name} --- {price}{unit}\n"
    if len(other_shops) != 0:
        text += "\n🧭 Можно попробовать зайти сюда:\n"
        for name, price, unit in other_shops:
            text += f"{name} -- {price}{unit}\n"
    if len(expired_top) != 0 or len(expired_other) != 0:
        expired = expired_other + expired_top
        for name in expired:
            text += f"❗ В {name} -- расписание закончилось, обнови данные. ❗ \n"
    return text


def build_list_text():
    SHOPS = load_shops()
    today = date.today()
    text = ""
    for shop in SHOPS:
        price = get_price(shop, today)
        if price is None:
            text += f"{shop['name']} -- Сегодня цена не указана (возможно завоз)\n"
        elif price == "Акция":
            text += f"{shop['name']} -- Акция\n"
        elif price == "expired":
            text += f"{shop['name']}: расписание цен закончилось, обнови данные\n"
        else:
            text += f"{shop['name']} -- {price}{shop['unit']}\n"
    return text

if __name__ == "__main__":
    print(date.today())
    for shop in load_shops():
        if shop["name"] == "Ква-ква":
            print(get_price(shop, date.today()))