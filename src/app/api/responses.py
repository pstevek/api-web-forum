from typing import List

from app.api.models import User, Post
from app.api.schemas import UserResponse, PostResponse
from fastapi.encoders import jsonable_encoder


def format_user_response(user: User) -> UserResponse:
    response = jsonable_encoder(user)
    response['role'] = user.role.name

    return UserResponse(**response)

def format_posts_response(posts: List[Post]) -> List[PostResponse]:
