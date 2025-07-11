import requests
from config import CONFIG

BIRDEYE_HEADERS = {
    "X-API-KEY": CONFIG["61bd77e007e04b42b9dc95dc842bf583"]
}

def get_new_tokens():
    url = "https://public-api.birdeye.so/public/tokenlist?sort_by=volume_24h"
    try:
        response = requests.get(url, headers=BIRDEYE_HEADERS)
        data = response.json()
        tokens = data.get("data", [])
        return [token for token in tokens if token.get("liquidity", 0) >= CONFIG["min_liquidity"]]
    except:
        return []
