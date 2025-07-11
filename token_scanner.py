import requests
from config import CONFIG

def get_verified_tokens():
    url = "https://public-api.birdeye.so/public/tokenlist?sort_by=created_at"
    headers = {"X-API-KEY": CONFIG["birdeye_api_key"]}

    try:
        res = requests.get(url, headers=headers)
        data = res.json()
        return [
            {"name": t["name"], "address": t["address"], "liquidity": t.get("liquidity", 0)}
            for t in data.get("data", [])
            if t.get("liquidity", 0) >= CONFIG["min_liquidity"]
        ]
    except:
        return []
