from sqlalchemy.orm import Session

from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    Header
)

from fastapi.security import OAuth2PasswordRequestForm

from app.core.dependencies import get_current_user
from app.database.dependencies import get_db

from app.models.user import User

from app.schemas.user import (
    UserCreate,
    Token
)

from app.core.security import (
    hash_password,
    verify_password
)

from app.core.auth import create_access_token


router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)


@router.post("/register")
def register(
    payload: UserCreate,
    db: Session = Depends(get_db)
):
    existing_username = (
        db.query(User)
        .filter(User.username == payload.username)
        .first()
    )

    if existing_username:
        raise HTTPException(
            status_code=400,
            detail="Username already exists"
        )

    existing_email = (
        db.query(User)
        .filter(User.email == payload.email)
        .first()
    )

    if existing_email:
        raise HTTPException(
            status_code=400,
            detail="Email already registered"
        )

    user = User(
    username=payload.username,
    email=payload.email,
    hashed_password=hash_password(
        payload.password
    ),
    role=payload.role
)

    db.add(user)
    db.commit()
    db.refresh(user)

    return {
        "message": "User created successfully"
    }


@router.post(
    "/login",
    response_model=Token
)
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    user = (
        db.query(User)
        .filter(
            User.username == form_data.username
        )
        .first()
    )

    if not user:
        raise HTTPException(
            status_code=401,
            detail="Invalid credentials"
        )

    if not verify_password(
        form_data.password,
        user.hashed_password
    ):
        raise HTTPException(
            status_code=401,
            detail="Invalid credentials"
        )

    access_token = create_access_token(
        {
            "sub": str(user.id),
            "username": user.username,
            "role": user.role
        }
    )

    return {
        "access_token": access_token,
        "token_type": "bearer"
    }


@router.get("/me")
def get_me(
    current_user=Depends(get_current_user)
):
    return current_user
