import secrets
from pydantic import BaseSettings


class Settings(BaseSettings):
    API_V1_STR: str
    PROJECT_NAME: str
    PROJECT_DESCRIPTION: str
    ALGORITHM: str
    SECRET_KEY: str = secrets.token_urlsafe(32)
    DB_NAME: str
    DB_USER: str
    DB_PASSWORD: str
    DB_HOST: str
    TOKEN_EXPIRY: int


settings = Settings()
