from fastapi import APIRouter, Depends, status
from fastapi.security import OAuth2PasswordRequestForm
from typing import Annotated
from app.api.dependencies import token_dependency
from app.api.services.user import user_service
from app.api.services.auth import auth_service
from app.api.schemas import UserCreate, UserResponse, TokenResponse
from datetime import timedelta

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post("/login", status_code=status.HTTP_200_OK, response_model=TokenResponse)
def login(request: Annotated[OAuth2PasswordRequestForm, Depends()]):
    authenticated_user = auth_service.authenticate_user(request)

    access_token = auth_service.create_access_token(
        data={"sub": authenticated_user.username, 'id': authenticated_user.id, 'role': authenticated_user.role.name},
        expires_delta=timedelta(minutes=200)
    )

    return TokenResponse(**{"access_token": access_token})


@router.post("/register", status_code=status.HTTP_201_CREATED, response_model=UserResponse)
def register(request: UserCreate):
    return user_service.create_user(request)


@router.get("/me", status_code=status.HTTP_200_OK, response_model=UserResponse)
def get_current_user(token: token_dependency):
    return auth_service.get_current_user(token)
