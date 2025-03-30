import pytest
from fastapi.testclient import TestClient

from tests.helpers import get_random_string
from tests.routers.helpers import authenticate, default_headers_with_token


class Test_UserRouter:
    def test_ユーザ作成(self, client: TestClient):
        username = "user_" + get_random_string(8)
        request_json = {
            "username": username,
            "email": f"{username}@example.com",
            "password": "tanaka",
        }
        response = client.post("/users", json=request_json)
        response_json = response.json()

        assert response.status_code == 200, response_json
        assert response_json["id"] > 0

    def test_ユーザ情報取得(self, client: TestClient):
        token = authenticate(client)
        headers = {"Authorization": f"Bearer {token}"}
        response = client.get("/users/me", headers=headers)
        assert response.status_code == 200
