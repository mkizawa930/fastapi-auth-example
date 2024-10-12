from fastapi.testclient import TestClient


def default_headers_with_token(headers: dict, token: str):
    headers["Authorization"] = f"Bearer: {token}"
    return headers

def authenticate(client: TestClient):
    response = client.post("/login", data={"username": "testuser@example.com", "password": "password"})
    if response.status_code != 200:
        raise Exception("authentication failed")
    token_data = response.json()
    access_token = token_data["access_token"]
    return access_token
