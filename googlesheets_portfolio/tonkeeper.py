import os
import json
import requests
from dotenv import load_dotenv

# load secret variables
load_dotenv()
TONKEEPER_ADDRESS_1 = os.getenv("TONKEEPER_ADDRESS_1")
TONKEEPER_ADDRESS_2 = os.getenv("TONKEEPER_ADDRESS_2")
COINSTATS_API = os.getenv("COINSTATS_API")

# tonkeeper wallet analysis using coinstats API

def analize_wallet(address, json_file):

    #creating the request
    tonkeeper_url = f"https://openapiv1.coinstats.app/wallet/balances?address={address}&networks=all"
    headers = {"accept": "application/json", "X-API-KEY":COINSTATS_API}
    response = requests.get(tonkeeper_url, headers=headers)
    tonkeeper_data = json.loads(response.text)

    #stracture and save the data
    data_to_save = {}
    wallet_total_balance = 0
    for entry in tonkeeper_data:
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
    with open(json_file, 'w') as file:
        json.dump(data_to_save, file, indent=4)
    print(f"Data was saved to {json_file}")

def main():
    analize_wallet(TONKEEPER_ADDRESS_1, 'tonkeeper_1.json')
    analize_wallet(TONKEEPER_ADDRESS_2, 'tonkeeper_2.json')

main()

