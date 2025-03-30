import pytest
from fastapi.testclient import TestClient

from app import models
from app.database import get_db
from app.main import app
from tests.conftest import get_test_db
from tests.database import test_engine

app.dependency_overrides[get_db] = get_test_db
test_client = TestClient(app)


@pytest.fixture(scope="session", autouse=True)
def setup_and_teardown():
    # setup
    yield


@pytest.fixture(scope="session")
def client() -> TestClient:
    return test_client
