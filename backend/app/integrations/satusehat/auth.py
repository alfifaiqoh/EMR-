import requests

from app.core.config import settings


def get_satusehat_token():

    response = requests.post(
        settings.SATUSEHAT_TOKEN_URL,
        data={
            "grant_type": "client_credentials",
            "client_id": settings.SATUSEHAT_CLIENT_ID,
            "client_secret": settings.SATUSEHAT_CLIENT_SECRET
        },
        headers={
            "Content-Type":
            "application/x-www-form-urlencoded"
        }
    )

    response.raise_for_status()

    return response.json()["access_token"]