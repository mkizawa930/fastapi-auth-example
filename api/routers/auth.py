from typing import Annotated

from api.crud import user_crud
from api.exceptions import PasswordMismatch
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from api import crud, schemas
from api.database import get_db
from api.routers.auth_helper import JWTer, PasswordHasher, get_jwter, get_password_hasher
from pydantic import EmailStr, SecretStr

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


async def get_current_user(
    token: str = Depends(oauth2_scheme),
    jwter=Depends(get_jwter),
) -> schemas.User:
    decoded_payload = jwter.decode(token)
    return schemas.LoginUser(username=decoded_payload["username"])


router = APIRouter(tags=["Authentication"])


@router.post("/login")
async def login(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    db=Depends(get_db),
    hasher: PasswordHasher = Depends(get_password_hasher),
    jwter: JWTer = Depends(get_jwter),
):
    try:
        db_user = user_crud.get_user_by_email(db, email=form_data.username)
        if hasher.hash_password(form_data.password) != db_user.password_hashed:
            raise HTTPException(status_code=401, detail="password mismtach")
        access_token = jwter.encode(username=db_user.username)
        return schemas.TokenData(access_token=access_token, token_type="bearer")
    except Exception as e:
        raise HTTPException(500, detail=f"error: {e}")
