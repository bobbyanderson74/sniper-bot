import requests
from config import CONFIG

def send_telegram_alert(message):
    url = f"https://api.telegram.org/bot{CONFIG['telegram_bot_token']}/sendMessage"
    data = {
        "chat_id": CONFIG["telegram_chat_id"],
        "text": message
    }
    requests.post(url, data=data)