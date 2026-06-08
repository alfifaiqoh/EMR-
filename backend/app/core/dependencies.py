from fastapi import (
    Depends,
    HTTPException,
    status
)

from fastapi.security import (
    OAuth2PasswordBearer
)

from app.core.auth import (
    decode_access_token
)


oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/auth/login"
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
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token"
        )

    return payload


def require_roles(*allowed_roles):
    """
    Example:

    require_roles("SUPER_ADMIN")

    require_roles(
        "SUPER_ADMIN",
        "ADMIN"
    )

    require_roles(
        "SUPER_ADMIN",
        "ADMIN",
        "DOCTOR"
    )
    """

    def role_checker(
        current_user=Depends(
            get_current_user
        )
    ):
        user_role = current_user.get(
            "role"
        )

        if user_role not in allowed_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Access denied"
            )

        return current_user

    return role_checker


def require_super_admin(
    current_user=Depends(
        get_current_user
    )
):
    if current_user["role"] != "SUPER_ADMIN":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only Super Admin can access"
        )

    return current_user


def require_admin(
    current_user=Depends(
        get_current_user
    )
):
    if current_user["role"] not in [
        "SUPER_ADMIN",
        "ADMIN"
    ]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only Admin can access"
        )

    return current_user


def require_doctor(
    current_user=Depends(
        get_current_user
    )
):
    if current_user["role"] not in [
        "SUPER_ADMIN",
        "ADMIN",
        "DOCTOR"
    ]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only Doctor can access"
        )

    return current_user