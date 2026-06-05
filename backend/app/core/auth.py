from datetime import datetime, timedelta

from jose import JWTError, jwt
from fastapi import HTTPException, status

from app.core.config import settings


SECRET_KEY = settings.SECRET_KEY
ALGORITHM = settings.ALGORITHM
ACCESS_TOKEN_EXPIRE_MINUTES = (
    settings.ACCESS_TOKEN_EXPIRE_MINUTES
)

def create_access_token(
    data: dict
):
    to_encode = data.copy()

    expire = (
        datetime.utcnow()
        + timedelta(
            minutes=ACCESS_TOKEN_EXPIRE_MINUTES
        )
    )

    to_encode.update(
        {"exp": expire}
    )

    return jwt.encode(
        to_encode,
        SECRET_KEY,
        algorithm=ALGORITHM
    )
from jose import JWTError

def decode_access_token(token: str):
    try:
        print("TOKEN MASUK:", token)

        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )

        print("PAYLOAD DECODE:", payload)

        return payload

    except JWTError as e:
        print("JWT ERROR:", str(e))

        raise HTTPException(
            status_code=401,
            detail="Invalid token"
        )