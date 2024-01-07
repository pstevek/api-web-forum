from datetime import datetime

from pydantic import BaseModel, EmailStr
from typing import List


# User
class BaseUser(BaseModel):
    id: int | None = None
    first_name: str
    last_name: str
    username: str
    email: EmailStr


class UserCreate(BaseUser):
    password: str

    class Config:
        orm_mode = True


class UserUpdate(BaseModel):
    first_name: str | None = None
    last_name: str | None = None
    email: EmailStr | None = None
    password: str | None = None


class UserResponse(BaseUser):
    role: str | None = None


# Comment
class BaseComment(BaseModel):
    content: str


class CommentCreate(BaseComment):
    pass


class CommentUpdate(BaseComment):
    pass


class CommentResponse(BaseComment):
    user: str
    post_slug: str


class LikeResponse(BaseModel):
    user: str
    post_slug: str


# Post
class BasePost(BaseModel):
    id: int | None = None
    title: str
    content: str
    created_at: datetime | None = None
    updated_at: datetime | None = None
    deleted_at: datetime | None = None


class PostCreate(BasePost):
    slug: str | None = None


class PostUpdate(BaseModel):
    is_misleading: bool


class PostResponse(BasePost):
    slug: str
    user: str
    is_misleading: bool
    likes: List[LikeResponse] = []
    comments: List[CommentResponse] = []
    total_likes: int | None = 0
    total_comments: int | None = 0


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"


