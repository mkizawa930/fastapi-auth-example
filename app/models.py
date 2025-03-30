from sqlalchemy import Column, DateTime, Integer, String, Text, func

from app.database import Base


class CustomModelMixin:
    created_at = Column(DateTime(timezone=True), default=func.now())
    updated_at = Column(DateTime(timezone=True), default=func.now())


class User(CustomModelMixin, Base):
    """User
    Attributes:
        - id(int)
        - username(str)
        - email(str)
        - password_hashed(str)
    """

    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String, nullable=False, index=True)
    email = Column(String, nullable=False, unique=True, index=True)
    password_hashed = Column(String, nullable=False)
