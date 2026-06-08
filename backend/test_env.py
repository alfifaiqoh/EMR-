from dotenv import load_dotenv
import os

load_dotenv()

client_id = os.getenv("SATUSEHAT_CLIENT_ID")
client_secret = os.getenv("SATUSEHAT_CLIENT_SECRET")

print("CLIENT_ID:", client_id)
print("CLIENT_SECRET:", client_secret[:5] + "..." if client_secret else None)