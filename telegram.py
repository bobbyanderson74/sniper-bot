import requests
from config import CONFIG

def send_telegram_alert(msg):
    url = f"https://api.telegram.org/bot{CONFIG['telegram_bot_token']}/sendMessage"
    data = {"chat_id": CONFIG["telegram_chat_id"], "text": msg}
    requests.post(url, data=data)
