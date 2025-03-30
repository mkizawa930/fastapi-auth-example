from contextlib import contextmanager

from loguru import logger

from app import models
from app.api.endpoints.auth_helper import PasswordHasher
from app.database import SessionLocal


@contextmanager
def get_db():
    db = SessionLocal()
    yield db
    db.close()


def create_user():
    password_hasher = PasswordHasher()
    with get_db() as db:
        try:
            db_user = models.User(
                username="admin",
                email="admin@example.com",
                password_hashed=password_hasher.hash_password("password"),
            )
            print(db_user.username)
            db.add(db_user)
            db.commit()
        except Exception as e:
            logger.error(e)
            db.rollback()


if __name__ == "__main__":
    create_user()
