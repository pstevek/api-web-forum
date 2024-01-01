import traceback
from fastapi import HTTPException, status
from app.api.repositories.user import user_repository
from app.api.schemas import UserCreate, UserUpdate
from app.api.models import User


class UserService:
    def __init__(self):
        self.repository = user_repository

    def create_user(self, request: UserCreate) -> User | HTTPException:
        try:
            return self.repository.create(user_request=request)
        except Exception:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error occurred while performing request :: {traceback.format_exc()}"
            )

    def update_user(self, request: UserUpdate, user: User) -> User | HTTPException:
        try:
            return self.repository.update(user_request=request, user=user)
        except Exception:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error occurred while performing request :: {traceback.format_exc()}"
            )


user_service = UserService()
