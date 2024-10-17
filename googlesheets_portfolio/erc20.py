import os
import json
import requests
from dotenv import load_dotenv

# load secret variables

load_dotenv()

COINMARKETCAP_API = os.getenv("COINMARKET_CAP_API")
COINSTATS_API = os.getenv("COINSTATS_API")
ERC_WALLET = os.getenv("ERC_WALLET_ADDRESS")

# erc-20 wallet analysis using coinstats API

erc_url = f"https://openapiv1.coinstats.app/wallet/balances?address={ERC_WALLET}&networks=all"
headers = {"accept": "application/json", "X-API-KEY":COINSTATS_API}
response = requests.get(erc_url, headers=headers)
ERC_data = json.loads(response.text)

data_to_save = {}

wallet_total_balance = 0

for entry in ERC_data:
    blockchain = entry["blockchain"]
    print(f"Blockchain: {blockchain}")
    total_balance = 0
    tokens = []
    for balance in entry["balances"]:
        symbol = balance["symbol"]
        amount = balance["amount"]
        price = balance["price"]
        total_balance = round(amount * price, 2) 
        print(f"Symbol: {symbol}")
        print(f"Amount: {amount}")
        print(f"Total: {total_balance}$")
        wallet_total_balance += total_balance
        tokens.append({
            "Symbol": symbol,
            "Amount": amount,
            "Price": price,
            "Total": total_balance
        })
    data_to_save[blockchain] = tokens
    print("\n")

#saving data to JSON

data_to_save["Wallet Balance"] = wallet_total_balance
with open('ERC_wallet_data_(065c).json', 'w') as file:
    json.dump(data_to_save, file, indent=4)

print("Data was saved to ERC_wallet_data_(065c).json")

        






