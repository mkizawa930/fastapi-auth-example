from typing import Annotated

from authlib.integrations.starlette_client import OAuth
from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from loguru import logger
from sqlalchemy.orm import Session

from app import models, schemas
from app.api.endpoints.auth_helper import JWTer, PasswordHasher, generate_access_token, get_jwter, get_password_hasher
from app.config import google_auth_config
from app.crud.user_crud import UserCrud
from app.database import get_db

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")

oauth = OAuth()
oauth.register(
    name="google",
    client_id=google_auth_config.client_id,
    client_secret=google_auth_config.client_secret,
    authorize_url="https://accounts.google.com/o/oauth2/v2/auth",
    access_token_url="https://oauth2.googleapis.com/token",
    jwks_uri="https://www.googleapis.com/oauth2/v3/certs",
    redirect_uri="http://localhost:8000/auth/google",
    client_kwargs={"scope": "openid profile email"},
)


async def get_current_user(
    token: str = Depends(oauth2_scheme),
    jwter=Depends(get_jwter),
) -> schemas.User:
    """ "現在のログインユーザーを取得する"""
    decoded_payload = jwter.decode(token)
    return schemas.LoginUser(username=decoded_payload["username"])


router = APIRouter(tags=["Authentication"])


@router.post("/login", description="フォームベースの認証")
async def auth(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    db=Depends(get_db),
    user_crud: UserCrud = Depends(UserCrud),
    hasher: PasswordHasher = Depends(get_password_hasher),
    jwter: JWTer = Depends(get_jwter),
):
    db_user = user_crud.get_user_by_email(db, email=form_data.username)
    if not db_user:
        raise HTTPException(status_code=404, detail="user not found")

    hashed_password = hasher.hash_password(form_data.password)
    if db_user.auth.password_hashed != hashed_password:
        raise HTTPException(status_code=401, detail="password mismtach")
    access_token = jwter.encode(username=db_user.username)
    return schemas.TokenData(access_token=access_token, token_type="bearer")


@router.get("/login/{provider}")
async def auth_with_provider(provider: str, request: Request):
    if provider == "google":
        google = oauth.create_client(provider)
        redirect_uri = request.url_for("authorize_google")
        return await google.authorize_redirect(request, redirect_uri)
    else:
        raise HTTPException(404, "provider not found")


@router.get("/auth/google")
async def authorize_google(
    request: Request,
    db: Session = Depends(get_db),
    user_crud: UserCrud = Depends(UserCrud),
    jwter: JWTer = Depends(get_jwter),
):
    google = oauth.create_client("google")
    token = await google.authorize_access_token(request)

    db_user = user_crud.find_user_by_email(db, email=token["userinfo"]["email"], auth_method=models.AuthMethod.Google)
    if not db_user:
        db_user = user_crud.create_user(
            db,
            username=token["userinfo"]["name"],
            email=token["userinfo"]["email"],
            provider="google",
        )

    access_token = generate_access_token(jwter, db_user)
    response = JSONResponse(content={"access_token": access_token, "token_type": "bearer"})
    response.set_cookie(key="access_token", value=access_token, httponly=True)
    return response
