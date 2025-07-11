import time
from token_scanner import get_new_tokens
from rugcheck import is_safe_token
from wallet import PhantomWallet
from telegram import send_telegram_alert
from config import CONFIG
from price_tracker import get_live_token_price

wallet = PhantomWallet(CONFIG["phantom_private_key"])

def run_sniper():
    send_telegram_alert("🚀 Live Sniper is running with REAL MONEY...")
    seen = set()

    while True:
        tokens = get_new_tokens()
        for token in tokens:
            if token["address"] in seen:
                continue
            seen.add(token["address"])

            if not is_safe_token(token["address"]):
                send_telegram_alert(f"❌ {token['name']} skipped (rug risk)")
                continue

            send_telegram_alert(f"🟢 Buying {token['name']} ({token['address']})...")
            tx = wallet.buy_token(token["address"], CONFIG["buy_amount_sol"])
            send_telegram_alert(f"✅ Bought {token['name']} – TX: {tx}")

            time.sleep(CONFIG["price_check_delay"])

            price_x = get_live_token_price(token["address"])
            send_telegram_alert(f"📈 {token['name']} is now at {price_x}x")

            if CONFIG["dynamic_selling"]:
                if price_x >= CONFIG["sell_multiplier"]:
                    sell_tx = wallet.sell_token(token["address"])
                    send_telegram_alert(f"💰 Sold {token['name']} at {price_x}x – TX: {sell_tx}")
                else:
                    send_telegram_alert(f"📊 Holding {token['name']} – rising trend")
            else:
                if price_x >= CONFIG["sell_multiplier"]:
                    sell_tx = wallet.sell_token(token["address"])
                    send_telegram_alert(f"💰 Sold {token['name']} at {price_x}x – TX: {sell_tx}")
        time.sleep(15)