from pydantic import BaseModel, ConfigDict, EmailStr, SecretStr


class CustomBaseModel(BaseModel):
    model_config = ConfigDict(
        # alias_generator=to_camel,
        populate_by_name=True,  # convert alias name
        from_attributes=True,  # construct from model class
    )


class LoginForm(BaseModel):
    email: EmailStr
    password: SecretStr


class TokenData(BaseModel):
    access_token: str
    token_type: str


class UserBase(BaseModel):
    email: EmailStr


class UserCreate(UserBase):
    username: str
    password: SecretStr


class User(UserBase):
    id: int
    username: str


class LoginUser(CustomBaseModel):
    username: str
