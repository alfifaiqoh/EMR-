import requests

from app.core.config import settings

from app.integrations.satusehat.auth import (
    get_satusehat_token
)


def satusehat_request(
    method: str,
    path: str,
    payload=None
):

    token = get_satusehat_token()

    url = (
        f"{settings.SATUSEHAT_BASE_URL}"
        f"/fhir-r4/v1{path}"
    )

    response = requests.request(
        method=method,
        url=url,
        json=payload,
        headers={
            "Authorization":
            f"Bearer {token}",
            "Content-Type":
            "application/fhir+json"
        }
    )

    response.raise_for_status()

    return response.json()