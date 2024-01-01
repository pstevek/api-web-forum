from app.api.models import User
from app.api.schemas import UserResponse
from fastapi.encoders import jsonable_encoder


def format_response(user: User) -> UserResponse:
    response = jsonable_encoder(user)
    response['role'] = user.role.name

    return UserResponse(**response)
