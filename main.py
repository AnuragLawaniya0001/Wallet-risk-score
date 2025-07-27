import requests
import csv
from datetime import datetime
import time


def get_wallet_data(wallet):
    url = f"https://api.ethplorer.io/getAddressInfo/{wallet}?apiKey=freekey"
    for attempt in range(3):
        response = requests.get(url)
        if response.status_code == 200:
            return response.json()
        elif response.status_code == 429:
            print(f"Rate limit hit. Waiting before retrying wallet {wallet}...")
            time.sleep(3)  # wait before retry
        else:
            print(f" Failed to fetch wallet {wallet}: HTTP {response.status_code}")
            break
    return None


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
        if (datetime.utcnow() - creation_date).days > 365:
            score += 200

    protocol_names = ["Aave", "Compound", "Uniswap", "Maker"]
    found_protocol = any(p.get("tokenInfo", {}).get("name", "") in protocol_names for p in tokens)
    if found_protocol:
        score += 300

    return min(score, 1000)

def process_wallet_list(file_path, output_csv="updated_wallet_scores.csv"):
    with open(file_path, 'r') as file:
        wallet_addresses = [line.strip() for line in file if line.strip()]

    print(f" Found {len(wallet_addresses)} wallets in file.")
    print("-" * 50)

    with open(output_csv, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['wallet_address', 'score'])

        for wallet in wallet_addresses:
            print(f" Scoring wallet: {wallet}")
            data = get_wallet_data(wallet)
            if data:
                score = calculate_risk_score(data)
                print(f" Risk Score: {score}/1000\n")
                writer.writerow([wallet, score])
            else:
                print(" Skipping due to error.\n")
                writer.writerow([wallet, "error"])
            time.sleep(1)  # Respect free API rate limit

if __name__ == "__main__":
    process_wallet_list("wallet_list.txt")
