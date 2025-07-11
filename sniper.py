import time
from token_scanner import get_verified_tokens
from rugcheck import is_safe_token
from wallet import PhantomWallet
from telegram import send_telegram_alert
from config import CONFIG
from price_tracker import get_live_token_price

wallet = PhantomWallet(CONFIG["phantom_private_key"], CONFIG["phantom_public_key"])

def run_sniper():
    send_telegram_alert("🚀 Advanced Sniper Bot is live...")
    seen = set()

    while True:
        tokens = get_verified_tokens()
        for token in tokens:
            if token["address"] in seen:
                continue
            seen.add(token["address"])

            if not is_safe_token(token["address"]):
                send_telegram_alert(f"❌ Skipped risky token {token['name']}")
                continue

            send_telegram_alert(f"🟢 Sniping {token['name']} ({token['address']})...")
            tx = wallet.buy_token(token["address"], CONFIG["buy_amount_sol"])
            if not tx:
                continue
            send_telegram_alert(f"✅ Bought {token['name']} – TX: {tx}")

            start_price = get_live_token_price(token["address"])
            peak_price = start_price
            sell_threshold = start_price * CONFIG["sell_multiplier"]

            for _ in range(15):
                time.sleep(CONFIG["price_check_delay"])
                current_price = get_live_token_price(token["address"])
                peak_price = max(peak_price, current_price)

                if current_price >= sell_threshold:
                    tx_sell = wallet.sell_token(token["address"])
                    send_telegram_alert(f"💰 Sold {token['name']} at {current_price:.2f}x – TX: {tx_sell}")
                    break
                elif current_price <= peak_price * 0.8:
                    tx_sell = wallet.sell_token(token["address"])
                    send_telegram_alert(f"⚠️ Trailing stop-sell {token['name']} at {current_price:.2f}x – TX: {tx_sell}")
                    break
