import pytest
from sqlalchemy.orm import Session

from app.api.endpoints.auth_helper import PasswordHasher
from app.crud.user_crud import UserCrud
from app.models import AuthMethod, GoogleAuth, PasswordAuth, User


class Test_UserCrud(object):
    @pytest.mark.parametrize(
        "username,email,provider,password",
        [
            ("testuser", "test@example.com", None, "password"),
        ],
    )
    def test_パスワード認証ユーザの作成(
        self,
        db: Session,
        user_crud: UserCrud,
        password_hasher: PasswordHasher,
        username: str,
        email: str,
        provider: str | None,
        password: str | None,
    ):
        if password:
            hashed_password = password_hasher.hash_password(password)

        db_user = user_crud.create_user(
            db,
            username=username,
            email=email,
            provider=provider,
            hashed_password=hashed_password,
        )

        assert db_user.id > 0
        auth = db_user.auth
        assert isinstance(auth, PasswordAuth)
        assert auth.hashed_password == hashed_password

    def test_Google認証ユーザーの作成(self, db: Session, user_crud: UserCrud):
        db_user = user_crud.create_user(
            db,
            username="testuser",
            email="test@example.com",
            provider="google",
        )

        assert db_user.id > 0
        assert isinstance(db_user.auth, GoogleAuth)

    def test_パスワード認証ユーザーの取得(self, db: Session, user_crud: UserCrud, password_hasher: PasswordHasher):
        db_user = User(
            username="testuser",
            email="test@example.com",
            auth=PasswordAuth(hashed_password=password_hasher.hash_password("password")),
        )
        db.add(db_user)
        db.flush()

        expected = db_user

        actual = user_crud.find_user_by_email(db, "test@example.com", AuthMethod.Password)
        assert actual
        assert actual.id == expected.id
        assert actual.username == expected.username
