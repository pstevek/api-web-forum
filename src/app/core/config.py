import secrets
from typing import List
from pydantic import BaseSettings, AnyHttpUrl, RedisDsn


class Settings(BaseSettings):
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str
    PROJECT_DESCRIPTION: str
    ALGORITHM: str
    SECRET_KEY: str = secrets.token_urlsafe(32)
    DB_NAME: str
    DB_USER: str
    DB_PASSWORD: str
    DB_HOST: str
    TOKEN_EXPIRY: int
    BACKEND_CORS_ORIGINS: List[AnyHttpUrl] = []
    DEBUG: bool = True
    SAMPLE_POST_API: AnyHttpUrl
    TZ: str
    REDIS_URL: RedisDsn
    CACHE_TTL: int


settings = Settings()
