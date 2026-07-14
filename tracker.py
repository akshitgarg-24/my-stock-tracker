```python
import os
import requests
from playwright.sync_api import sync_playwright

# ==============================
# SETTINGS
# ==============================

PINCODES = [
    "132001",
    "136118",
    "132103"
]

TRACKING_LINKS = [
    "https://amzn.in/d/0cuIjmaB",
    "https://amzn.in/d/0aGzZaHP",
    "https://dl.flipkart.com/dl/sony-playstation-5-console-825-gb/p/itm62f0f8b3c0bfb?pid=GMCGHMTYZ8BUBMFB",
    "https://dl.flipkart.com/dl/sony-playstation5-console-slim-cfi-2008a01x-cfi-2116a01y-1-tb/p/itm89489e2adcd2c",
    "https://neu.in/wiOpFNdJ53b",
    "https://neu.in/V7iineMRL4b",
    "https://neu.in/jo5OseORL4b",
    "https://www.vijaysales.com/p/252606/sony-playstationr5-disc-sa-e-edition-console-video-game-ps5r-slim",
    "https://www.vijaysales.com/p/254870/sony-playstationr5-digital-edition-console-video-game-825gb-ps5r-slim",
    "https://shopatsc.com/collections/all/products/playstation-5-standard-edition",
    "https://shopatsc.com/collections/all/products/playstation-5-digital-edition",
    "https://www.reliancedigital.in/product/sony-playstation-ps5-slim-console-luh1rv-7537998"
]


TELEGRAM_TOKEN = os.getenv("8648877037:AAEf4mZFj7Jj3KCKHGhvgxn_kDVIsTV-MP4")
TELEGRAM_CHAT_ID = os.getenv("887029148")


# ==============================
# TELEGRAM
# ==============================

def send_telegram(message):
    if not TELEGRAM_TOKEN or not TELEGRAM_CHAT_ID:
        print("Telegram credentials missing")
        return

    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"

    try:
        requests.post(
            url,
            json={
                "chat_id": TELEGRAM_CHAT_ID,
                "text": message
            },
            timeout=20
        )
    except Exception as e:
        print("Telegram error:", e)


# ==============================
# STOCK CHECK
# ==============================

def check_stock(page, url):

    try:
        page.goto(
            url,
            timeout=60000,
            wait_until="domcontentloaded"
        )

        content = page.content().lower()

        unavailable = [
            "out of stock",
            "currently unavailable",
            "sold out",
            "notify me",
            "coming soon"
        ]

        available = [
            "add to cart",
            "buy now",
            "in stock",
            "add to bag"
        ]


        if any(word in content for word in unavailable):
            return False


        if any(word in content for word in available):
            return True


        return False


    except Exception as e:
        print("Page error:", e)
        return False



# ==============================
# MAIN
# ==============================

def start_tracking():

    found = []

    with sync_playwright() as p:

        browser = p.chromium.launch(
            headless=True
        )

        context = browser.new_context(
            user_agent=
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
        )

        page = context.new_page()


        print("Starting PS5 tracker...")


        for url in TRACKING_LINKS:

            print("Checking:", url)

            if check_stock(page, url):

                print("STOCK FOUND:", url)

                found.append(url)


        browser.close()


    if found:

        message = (
            "🚨 PS5 STOCK ALERT 🚨\n\n"
            "Available products:\n\n"
            + "\n".join(found)
        )

        send_telegram(message)

    else:

        print("No stock found")


if __name__ == "__main__":
    start_tracking()
```
