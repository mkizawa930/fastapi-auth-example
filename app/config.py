from pydantic import ConfigDict
from pydantic_settings import BaseSettings


class GoogleAuthConfig(BaseSettings):
    client_id: str
    client_secret: str

    model_config = ConfigDict(
        env_file=".env",
        env_prefix="GOOGLE_",
        extra="ignore",
    )


google_auth_config = GoogleAuthConfig()
