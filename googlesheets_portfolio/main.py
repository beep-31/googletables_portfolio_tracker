import os.path
from datetime import datetime
import json
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]

SAMPLE_SPREADSHEET_ID = "1qXRcsg5kWta1GScwcEeRpqluvjBe88iC1_UNXi96NnI"

ERC_JSON_PATH = "ERC_wallet_data_(065c).json"
TONKEEPER_JSON_PATH = "tonkeeper_1.json"
TONKEEPER_2_JSON_PATH = "tonkeeper_2.json"

def update_spreadsheet(spreedsheet_name, json_path, sheet):

  with open(json_path, 'r') as file:
    data = json.load(file)
  values =[]
  for network, assets in data.items():
    if network == "Wallet Balance":
      continue
    for asset in assets:
      values.append([network, asset["Symbol"], asset["Amount"], asset["Price"], asset["Total"]])

  if "Wallet Balance" in data:
    wallet_balance = data["Wallet Balance"]
    values.append(["Wallet Balance", "", "", "", wallet_balance])
    
  body = {
    "values": values
  }

  update_range = spreedsheet_name + "!A2"
  sheet.values().update(
    spreadsheetId = SAMPLE_SPREADSHEET_ID,
    range = update_range,
    valueInputOption = "RAW",
    body = body
  ).execute()

  today = datetime.today().strftime("%Y-%m-%d")
  body = {
    "values": [[today]]
  }

  update_range = spreedsheet_name + "!A1"
  sheet.values().update(
    spreadsheetId = SAMPLE_SPREADSHEET_ID,
    range = update_range,
    valueInputOption = "RAW",
    body = body
  ).execute()

  print("The data was written successfully!")

def main():
  creds = None
  # The file token.json stores the user's access and refresh tokens, and is
  # created automatically when the authorization flow completes for the first
  # time.
  if os.path.exists("token.json"):
    creds = Credentials.from_authorized_user_file("token.json", SCOPES)
  # If there are no (valid) credentials available, let the user log in.
  if not creds or not creds.valid:
    if creds and creds.expired and creds.refresh_token:
      creds.refresh(Request())
    else:
      flow = InstalledAppFlow.from_client_secrets_file(
          "credentials.json", SCOPES
      )
      creds = flow.run_local_server(port=0)
    # Save the credentials for the next run
    with open("token.json", "w") as token:
      token.write(creds.to_json())

  try:
    service = build("sheets", "v4", credentials=creds)
    sheet = service.spreadsheets()
    update_spreadsheet('Metamask', ERC_JSON_PATH, sheet)
    update_spreadsheet('Tonkeeper', TONKEEPER_JSON_PATH, sheet)
    update_spreadsheet('Tonkeeper2', TONKEEPER_2_JSON_PATH, sheet)

  except HttpError as err:
    print(err)

if __name__ == "__main__":
  main()