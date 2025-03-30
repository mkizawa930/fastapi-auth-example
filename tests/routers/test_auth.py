import base64

from fastapi.testclient import TestClient


class Test_AuthRouter:
    def test_ログイン(self, client: TestClient):
        email = "testuser@example.com"
        password = "password"
        form = {"username": email, "password": password}
        response = client.post("/login", data=form)  # formログイン
        assert response.status_code == 200, response.json()

        got = response.json()
        assert len(got["access_token"]) > 0
        assert got["token_type"] == "bearer"
