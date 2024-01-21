from typing import Annotated
from fastapi import APIRouter, Depends, status
from fastapi.security import OAuth2PasswordRequestForm
from app.api.responses import format_user_response, format_token_response
from app.api.services.user import user_service
from app.api.services.auth import auth_service
from app.api.schemas import UserCreate, UserResponse, TokenResponse

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post("/login", status_code=status.HTTP_200_OK, response_model=TokenResponse)
def login(request: Annotated[OAuth2PasswordRequestForm, Depends()]):
    authenticated_user = auth_service.authenticate_user(request)

    access_token = auth_service.create_access_token(
        data={"sub": authenticated_user.username, 'id': authenticated_user.id, 'role': authenticated_user.role.name}
    )

    return format_token_response(access_token)


@router.post("/register", status_code=status.HTTP_201_CREATED, response_model=UserResponse)
def register(request: UserCreate):
    user = user_service.create_user(request)

    return format_user_response(user)

