from fastapi import (
    Depends,
    HTTPException,
    status
)

from fastapi.security import (
    OAuth2PasswordBearer
)
from fastapi.security import (
    OAuth2PasswordBearer
)

from app.core.auth import (
    decode_access_token
)

oauth2_scheme = (
    OAuth2PasswordBearer(
        tokenUrl="/auth/login"
    )
)


def get_current_user(
    token: str = Depends(
        oauth2_scheme
    )
):
    payload = decode_access_token(
        token
    )

    if not payload:
        raise HTTPException(
            status_code=(
                status
                .HTTP_401_UNAUTHORIZED
            ),
            detail=(
                "Invalid or expired token"
            )
        )

    return payload

def require_doctor(
    current_user=Depends(
        get_current_user
    )
):
    if (
        current_user["role"]
        != "DOCTOR"
    ):
        raise HTTPException(
            status_code=403,
            detail=(
                "Only doctor "
                "can access"
            )
        )

    return current_user


def require_admin(
    current_user=Depends(
        get_current_user
    )
):
    if (
        current_user["role"]
        != "ADMIN"
    ):
        raise HTTPException(
            status_code=403,
            detail=(
                "Only admin "
                "can access"
            )
        )

    return current_user