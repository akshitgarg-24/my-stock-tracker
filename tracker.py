import time
import random
import requests
from playwright.sync_api import sync_playwright

# =====================================================================
# ⚙️ EDIT ONLY THIS BLOCK BELOW (DO NOT TOUCH ANYTHING ELSE)
# =====================================================================

# Put your real Telegram Token between the quotation marks
TELEGRAM_TOKEN = "8648877037:AAFFTH0SmuLSt_kKvssG-a_tKGzSTJzIydU"

# Put your real Telegram Chat ID between the quotation marks
TELEGRAM_CHAT_ID = "887029148"

# Add all your pincodes inside the brackets, separated by commas
PINCODES = ["132001", "136118", "132103"] 

# Paste all 12 of your product web links here inside the quotes, separated by commas
TRACKING_LINKS = [
    "https://amzn.in/d/0cuIjmaB",
    "https://amzn.in/d/0aGzZaHP",
    "https://dl.flipkart.com/dl/sony-playstation-5-console-825-gb/p/itm62f0f8b3c0bfb?pid=GMCGHMTYZ8BUBMFB&lid=LSTGMCGHMTYZ8BUBMFBE2W9DE&marketplace=FLIPKART&_refId=&_appId=CL",
    "https://dl.flipkart.com/dl/sony-playstation5-console-slim-cfi-2008a01x-cfi-2116a01y-1-tb/p/itm89489e2adcd2c?pid=GMCGZCYPAFYBUNAR&lid=LSTGMCGZCYPAFYBUNARLIR5LG&marketplace=FLIPKART&_refId=&_appId=CL",
    "https://neu.in/wiOpFNdJ53b",
    "https://neu.in/V7iineMRL4b",
    "https://neu.in/jo5OseORL4b",
    "https://www.vijaysales.com/p/252606/sony-playstationr5-disc-sa-e-edition-console-video-game-ps5r-slim",
    "https://www.vijaysales.com/p/254870/sony-playstationr5-digital-edition-console-video-game-825gb-ps5r-slim",
    "https://shopatsc.com/collections/all/products/playstation-5-standard-edition",
    "https://shopatsc.com/collections/all/products/playstation-5-digital-edition",
    "https://www.reliancedigital.in/product/sony-playstation-ps5-slim-console-luh1rv-7537998"
]

# =====================================================================
# 🛑 STOP! DO NOT REMOVE, EDIT, OR TOUCH ANYTHING BELOW THIS LINE!
# =====================================================================

def send_telegram(message):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    try:
        requests.post(url, json={"chat_id": TELEGRAM_CHAT_ID, "text": message})
    except Exception as e:
        print(f"Telegram failed: {e}")

def is_item_available(page):
    content = page.content().lower()
    out_of_stock_phrases = ["out of stock", "currently unavailable", "notify me", "sold out", "coming soon"]
    in_stock_phrases = ["add to cart", "buy now", "add", "in stock", "delivery in"]

    if any(phrase in content for phrase in out_of_stock_phrases):
        return False
    if any(phrase in content for phrase in in_stock_phrases):
        return True
    return False

def start_tracking():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        )
        page = context.new_page()
        
        print(f"🚀 Initializing tracking for {len(TRACKING_LINKS)} links...")
        send_telegram(f"🚀 Live tracking started for {len(TRACKING_LINKS)} product URLs!")

        while True:
            for url in TRACKING_LINKS:
                for pin in PINCODES:
                    print(f"🔎 Checking Pincode {pin} on: {url[:40]}...")
                    try:
                        page.goto(url, timeout=60000)
                        page.wait_for_load_state("domcontentloaded")
                        
                        if is_item_available(page):
                            alert_msg = f"🚨 ITEM DETECTED IN STOCK!\n📍 Pincode: {pin}\n🔗 Link: {url}"
                            print(alert_msg)
                            send_telegram(alert_msg)
                            
                    except Exception as e:
                        print(f"⚠️ Error loading page: {e}")
                    
                    time.sleep(random.randint(2, 5))

            sleep_time = random.randint(20, 40)
            print(f"💤 Cycle finished. Sleeping for {sleep_time}s...")
            time.sleep(sleep_time)

if __name__ == "__main__":
    start_tracking()
