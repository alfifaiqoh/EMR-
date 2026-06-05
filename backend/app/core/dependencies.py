from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer

from app.core.auth import decode_access_token

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/auth/login"
)


def get_current_user(
    token: str = Depends(oauth2_scheme)
):
    print("TOKEN DITERIMA:", token)

    payload = decode_access_token(token)

    print("PAYLOAD:", payload)

    return payload