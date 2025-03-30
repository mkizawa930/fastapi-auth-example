from logging import getLogger

from pydantic import EmailStr
from sqlalchemy.exc import NoResultFound, SQLAlchemyError
from sqlalchemy.orm import Session

from app import models

logger = getLogger("crud.users")


def create_user(
    db: Session,
    username: str,
    email: EmailStr,
    password_hashed: str,
) -> models.User:
    db_user = models.User(username=username, email=email, password_hashed=password_hashed)
    db.add(db_user)
    db.commit()
    return db_user


def get_user_by_email(db: Session, email: EmailStr) -> models.User:
    db_user = db.query(models.User).filter_by(email=email).one()
    return db_user


def delete_user(db: Session, user: models.User):
    db.delete(user)
    db.commit()
