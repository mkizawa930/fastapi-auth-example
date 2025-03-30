from typing import Annotated

from authlib.integrations.starlette_client import OAuth
from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

from app import schemas
from app.config import google_auth_config
from app.crud import user_crud
from app.database import get_db
from app.api.endpoints.auth_helper import JWTer, PasswordHasher, get_jwter, get_password_hasher
from loguru import logger

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


@router.get("/login/{provider}")
async def auth_with_provider(provider: str, request: Request):
    if provider == "google":
        google = oauth.create_client(provider)
        redirect_uri = request.url_for("authorize_google")
        return await google.authorize_redirect(request, redirect_uri)
    else:
        raise HTTPException(404, "provider not found")


@router.get("/auth/google")
async def authorize_google(request: Request, jwter: JWTer = Depends(get_jwter)):
    google = oauth.create_client("google")
    token = await google.authorize_access_token(request)
    # get user info
    return {"access_token": ""}
