import os
import requests
from dotenv import load_dotenv
from requests.auth import HTTPBasicAuth

load_dotenv()

client_id = os.getenv("SATUSEHAT_CLIENT_ID")
client_secret = os.getenv("SATUSEHAT_CLIENT_SECRET")

url = "https://api-satusehat-stg.dto.kemkes.go.id/oauth2/v1/accesstoken?grant_type=client_credentials"

response = requests.post(
    url,
    auth=HTTPBasicAuth(client_id, client_secret),
    headers={
        "Content-Type": "application/x-www-form-urlencoded"
    }
)

print("Status:", response.status_code)
print(response.text)