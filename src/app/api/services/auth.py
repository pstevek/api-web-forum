import traceback
from typing import Annotated
from app.api.repositories.user import user_repository
from datetime import datetime, timedelta
from app.core.config import settings
from app.api.models import User
from app.api.dependencies import pwd_context, token_dependency
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from jose import jwt, JWTError

secret_key = settings.SECRET_KEY
algorithm = settings.ALGORITHM
token_expiry = settings.TOKEN_EXPIRY


class AuthService:
    def __init__(self):
        self.repository = user_repository

    @staticmethod
    def create_access_token(data: dict) -> str:
        expire = datetime.utcnow() + timedelta(minutes=token_expiry)
        to_encode = data.copy()
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, secret_key, algorithm=algorithm)

        return encoded_jwt

    def authenticate_user(self, request: Annotated[OAuth2PasswordRequestForm, Depends()]) -> User:
        try:
            user = self.repository.get_by_username(request.username)
        except Exception:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error occurred while performing request :: {traceback.format_exc()}"
            )

        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
        # Authenticate user
        if not pwd_context.verify(request.password, user.password):
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect username or password")

        return user

    def get_current_user(self, token: token_dependency) -> User:
        try:
            payload = jwt.decode(token, secret_key, algorithms=[algorithm])
            username: str = payload.get('sub')
            user_id: int = payload.get('id')

            if all(field is None for field in [username, user_id]):
                raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Could not authenticate user.')

            user = self.repository.get(model_id=user_id)

            if not user:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

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


auth_service = AuthService()
