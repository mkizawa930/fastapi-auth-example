from logging import getLogger

from pydantic import EmailStr
from sqlalchemy import and_, select
from sqlalchemy.exc import NoResultFound, SQLAlchemyError
from sqlalchemy.orm import Session

from app import models

logger = getLogger("crud.users")


class UserCrud(object):
    def create_user(
        self,
        db: Session,
        username: str,
        email: EmailStr,
        provider: str | None = None,
        hashed_password: str | None = None,
    ) -> models.User:
        match provider:
            case "google":
                auth = models.GoogleAuth()
            case _:
                auth = models.PasswordAuth(hashed_password=hashed_password)

        db_user = models.User(username=username, email=email, auth=auth)
        db.add(db_user)
        db.flush()
        db.refresh(db_user)
        return db_user

    def find_user_by_email(
        self,
        db: Session,
        email: EmailStr,
        auth_method: models.AuthMethod,
    ) -> models.User | None:
        stmt = (
            select(models.User)
            .join(models.Auth)
            .where(
                and_(
                    models.User.email == email,
                    models.Auth.auth_method == auth_method,
                )
            )
        )
        return db.scalars(stmt).first()

    def delete_user(self, db: Session, user: models.User):
        db.delete(user)
        db.commit()
