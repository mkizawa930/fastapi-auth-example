from typing import Generator

from app.database import get_db
import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.main import app
from app.api.endpoints.auth_helper import PasswordHasher
from app.crud.user_crud import UserCrud
from app.models import Base
from tests.database import TestSessionLocal, engine, get_test_db

app.dependency_overrides[get_db] = get_test_db
test_client = TestClient(app)


@pytest.fixture(scope="session", autouse=True)
def setup_and_teardown():
    Base.metadata.create_all(bind=engine)

    yield

    Base.metadata.droop_all(bind=engine)


@pytest.fixture(scope="function")
def db() -> Generator[Session, None, None]:
    db = TestSessionLocal()
    yield db
    db.close()


@pytest.fixture(scope="session")
def client() -> TestClient:
    return test_client


@pytest.fixture(scope="session")
def password_hasher() -> Generator[PasswordHasher, None, None]:
    return PasswordHasher()


@pytest.fixture(scope="function")
def user_crud() -> Generator[UserCrud, None, None]:
    return UserCrud()
