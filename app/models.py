from enum import StrEnum

from sqlalchemy import (Column, DateTime, Enum, ForeignKey, Integer, String,
                        Text, func)
from sqlalchemy.orm import relationship

from app.database import Base


class AuthMethod(StrEnum):
    Password = "password"
    Google = "google"


class CustomModelMixin:
    created_at = Column(DateTime(timezone=True), default=func.now())
    updated_at = Column(DateTime(timezone=True), default=func.now())


class User(CustomModelMixin, Base):
    """User
    Attributes:
        - id(int)
        - username(str)
        - email(str)
    """

    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String, nullable=False, index=True)
    email = Column(String, nullable=False, unique=True, index=True)
    auth = relationship(
        "Auth",
        back_populates="user",
        uselist=False,
    )


class Auth(CustomModelMixin, Base):
    """UserAuth
    Attributes:
        - id(int)
        - user_id(int)
        - provider(str)
        - provider_id(str)
    """

    __tablename__ = "auth"
    __mapper_args__ = {"polymorphic_identity": "auth", "polymorphic_on": "auth_method"}

    id = Column(Integer, primary_key=True)
    user_id = Column(ForeignKey("users.id"), nullable=False)
    user = relationship("User", back_populates="auth")
    auth_method = Column(Enum(AuthMethod), nullable=False)


class PasswordAuth(Auth):
    __tablename__ = "password_auth"
    __mapper_args__ = {"polymorphic_identity": "password"}

    id = Column(Integer, ForeignKey("auth.id"), primary_key=True)
    hashed_password = Column(String, nullable=False)


class GoogleAuth(Auth):
    __tablename__ = "google_auth"
    __mapper_args__ = {"polymorphic_identity": "google"}

    id = Column(Integer, ForeignKey("auth.id"), primary_key=True)
