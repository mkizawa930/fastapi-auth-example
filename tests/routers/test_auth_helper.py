from api.routers.auth_helper import JWTer, PasswordHasher
from pydantic import SecretStr


class Test_PasswordHahser:
    def test_パスワードのハッシュ化(self):
        hasher = PasswordHasher()
        password_hashed = hasher.hash_password("hoge")
        assert isinstance(password_hashed, str)


class Test_JWTer:
    
    def test_JWTトークンの生成(self):
        jwter = JWTer()
        token = jwter.encode(username="testuser@example.com")
        decoded = jwter.decode(token)
        assert decoded["username"] == "testuser@example.com"
        