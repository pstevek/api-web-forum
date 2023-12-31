import traceback
from fastapi import HTTPException, status
from fastapi.encoders import jsonable_encoder
from app.api.repositories.user import user_repository
from app.api.schemas import UserCreate, UserResponse


class UserService:
    def __init__(self):
        self.repository = user_repository

    def create_user(self, request: UserCreate) -> UserResponse | HTTPException:
        try:
            new_user = self.repository.create(user_request=request)

            response = jsonable_encoder(new_user)
            response['role'] = new_user.role.name

            return UserResponse(**response)
        except Exception:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error occurred while performing request :: {traceback.format_exc()}"
            )


user_service = UserService()
