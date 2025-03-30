from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import schemas
from app.api.endpoints.auth import get_current_user
from app.api.endpoints.auth_helper import PasswordHasher, get_password_hasher
from app.crud import user_crud
from app.database import get_db

router = APIRouter(tags=["Users"])


@router.post(
    "/users",
    response_model=schemas.User,
)
async def create_user(
    user_create: schemas.UserCreate,
    db: Session = Depends(get_db),
    password_hasher: PasswordHasher = Depends(get_password_hasher),
):
    try:
        password_hashed = password_hasher.hash_password(user_create.password)
        db_user = user_crud.create_user(
            db,
            username=user_create.username,
            email=user_create.email,
            password_hashed=password_hashed,
        )
        return db_user
    except Exception as e:
        raise HTTPException(500, detail=e)


@router.get(
    "/users/me",
    response_model=schemas.LoginUser,
)
async def get_users_me(current_user: schemas.LoginUser = Depends(get_current_user)):
    return current_user
