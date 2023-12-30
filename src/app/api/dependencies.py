import traceback

from typing import Annotated
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from datetime import datetime, timedelta
from jose import jwt, JWTError
from src.app.core.config import settings
from src.app.core.database import db_dependency
from src.app.core.config import settings
from src.app.api.models import User
from src.app.api.repositories.user import user_repository
from passlib.context import CryptContext

secret_key = settings.SECRET_KEY
algorithm = settings.ALGORITHM
token_expiry = settings.TOKEN_EXPIRY
oauth2_bearer = OAuth2PasswordBearer(tokenUrl='auth/token')
token_dependency = Annotated[str, Depends(oauth2_bearer)]
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def create_access_token(data: dict, expires_delta: timedelta | None = None) -> str:
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=15))
    to_encode = data.copy()
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, secret_key, algorithm=algorithm)

    return encoded_jwt


def get_current_user(token: token_dependency, db: db_dependency) -> User:
    try:
        payload = jwt.decode(token, secret_key, algorithms=[algorithm])
        username: str = payload.get('sub')
        user_id: int = payload.get('id')

        if username is None or user_id is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Could not authenticate user.')

        user = user_repository.get(user_id=user_id)

        return user
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token has expired. Please login again."
        )
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error extracting user information :: {traceback.format_exc()}"
        )
