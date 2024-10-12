from logging import getLogger

from pydantic import EmailStr, SecretStr
from sqlalchemy.exc import IntegrityError, NoResultFound, SQLAlchemyError
from sqlalchemy.orm import Session

from api import models
from api.exceptions import DatabaseError, ResourceNotFound

logger = getLogger("crud.users")


def create_user(
    db: Session,
    username: str,
    email: EmailStr,
    password_hashed: str,
) -> models.User:
    db_user = models.User(username=username, email=email, password_hashed=password_hashed)
    try:
        db.add(db_user)
        db.commit()
        return db_user
    except Exception as e:
        logger.error(f"{e}")


def get_user_by_email(db: Session, email: EmailStr) -> models.User:
    try:
        db_user = db.query(models.User).filter_by(email=email).one()
        return db_user
    except NoResultFound as e:
        raise ResourceNotFound()
    except SQLAlchemyError as e:
        raise DatabaseError(e)
    except Exception as e:
        logger.error(e)
        raise e


def delete_user(db: Session, user: models.User):
    try:
        db.delete(user)
        db.commit()
    except SQLAlchemyError as e:
        raise DatabaseError(e)
    except Exception as e:
        logger.error(e)
        raise e
