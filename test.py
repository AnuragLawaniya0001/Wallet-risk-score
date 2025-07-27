import requests
from datetime import datetime

ETHPLORER_API = "https://api.ethplorer.io/getAddressInfo/{}?apiKey=freekey"

def get_wallet_info(wallet_address):
    url = ETHPLORER_API.format(wallet_address)
    response = requests.get(url)
    return response.json() if response.status_code == 200 else None

def calculate_risk_score(wallet_data):
    score = 0

    eth_balance = wallet_data.get("ETH", {}).get("balance", 0)
    if eth_balance > 0:
        score += 200

    tokens = wallet_data.get("tokens", [])
    if tokens:
        score += 150

    txn_count = wallet_data.get("countTxs", 0)
    if txn_count > 10:
        score += 150

    created_at = wallet_data.get("contractInfo", {}).get("creationDate")
    if created_at:
        creation_date = datetime.utcfromtimestamp(created_at)
        age_years = (datetime.utcnow() - creation_date).days / 365
        if age_years > 1:
            score += 200

    protocol_names = ["Aave", "Compound", "Uniswap", "Maker"]
    found_protocol = any(p.get("tokenInfo", {}).get("name", "") in protocol_names for p in tokens)
    if found_protocol:
        score += 300

    return min(score, 1000)

if __name__ == "__main__":
    wallet_address = "0xded1f838ae6aa5fcd0f13481b37ee88e5bdccb3d"  
    data = get_wallet_info(wallet_address)

    if data:
        score = calculate_risk_score(data)
        print(f" Wallet: {wallet_address}")
        print(f" Risk Score: {score}/1000")
    else:
        print(" Failed to fetch wallet data.")
