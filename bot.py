import requests
from bs4 import BeautifulSoup
import time

BOT_TOKEN = "8704782405:AAFhK5_2piJOa5zWMPki_YAXkbBemAJWjsI"
CHAT_ID = "8159809991"

# 🔥 Add multiple product URLs here
PRODUCTS = [
    {
        "name": "Hot Wheels Car Culture",
        "url": "https://www.karzanddolls.com/details/hot+wheels/car-culture/MTEx"
    },
    {
        "name": "Hot Wheels Boulevard",
        "url": "https://www.karzanddolls.com/details/hot+wheels/boulevard-series/MTIw"
    },
    {
        "name": "Hot Wheels FnF",
        "url": "https://www.karzanddolls.com/details/hot+wheels/fast-and-furious/MTEz"
    }
]

def send_telegram_message(message):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    data = {
        "chat_id": CHAT_ID,
        "text": message
    }
    requests.post(url, data=data)

def check_stock(url):
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")

    if "out of stock" in soup.text.lower():
        return False
    return True

# Track alerts per product
alerted = {product["url"]: False for product in PRODUCTS}

print("🔄 Bot started...")

while True:
    for product in PRODUCTS:
        in_stock = check_stock(product["url"])

        if in_stock:
            if not alerted[product["url"]]:
                send_telegram_message(
                    f"🚀 RESTOCK ALERT!\n\n{product['name']}\n{product['url']}"
                )
                alerted[product["url"]] = True
        else:
            alerted[product["url"]] = False

    time.sleep(300)
