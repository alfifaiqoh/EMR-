import requests

CLIENT_ID = "CLIENT_ID_ANDA"
CLIENT_SECRET = "CLIENT_SECRET_ANDA"

url = "https://api-satusehat-stg.dto.kemkes.go.id/oauth2/v1/accesstoken?grant_type=client_credentials"

response = requests.post(
    url,
    auth=(CLIENT_ID, CLIENT_SECRET)
)

print("Status:", response.status_code)
print(response.text)