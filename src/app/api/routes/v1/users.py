from fastapi import APIRouter
from starlette import status
from app.api.dependencies import token_dependency
from app.api.schemas import UserUpdate, UserResponse
from app.api.services.auth import auth_service
from app.api.services.user import user_service
from app.api.responses import format_user_response

router = APIRouter(prefix="/users", tags=["User Management"])


@router.get("/me", status_code=status.HTTP_200_OK, response_model=UserResponse)
def get_current_user(token: token_dependency):
    current_user = auth_service.get_current_user(token)

    return format_user_response(current_user)


@router.put("/me", status_code=status.HTTP_200_OK, response_model=UserResponse)
def update_current_user(token: token_dependency, request: UserUpdate):
    user = auth_service.get_current_user(token)

    updated_user = user_service.update_user(request=request, user=user)

    return format_user_response(updated_user)
