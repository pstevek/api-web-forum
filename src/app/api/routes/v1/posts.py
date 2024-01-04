from typing import List
from fastapi import APIRouter, status
from isort import comments

from app.api import responses
from app.api.dependencies import token_dependency
from app.api.schemas import PostResponse, PostCreate, CommentCreate
from app.api.services.auth import auth_service
from app.api.services.post import post_service

router = APIRouter(prefix="/posts", tags=["Post Management"])


@router.get("", status_code=status.HTTP_200_OK, response_model=List[PostResponse])
async def get_all_posts(skip: int = 0, limit: int = 100):
    posts = post_service.get_all_posts(skip=skip, limit=limit)

    return responses.format_posts_response(posts)


@router.get("/{post_slug}", status_code=status.HTTP_200_OK, response_model=PostResponse)
async def get_post(post_slug: str):
    post = post_service.get_post_by_slug(post_slug)

    return responses.format_post_response(post)


@router.post("", status_code=status.HTTP_201_CREATED, response_model=PostResponse)
async def create_user_post(token: token_dependency, request: PostCreate):
    user = auth_service.get_current_user(token)
    new_post = post_service.create_user_post(user, request)

    return responses.format_post_response(new_post)


@router.post("/{post_slug}/comment", status_code=status.HTTP_201_CREATED, response_model=PostResponse)
async def create_post_comment(post_slug: str, token: token_dependency, request: CommentCreate):
    user = auth_service.get_current_user(token)
    updated_post = post_service.create_post_comment(post_slug, user, request)

    return responses.format_post_response(updated_post)


@router.post("/{post_slug}/like", status_code=status.HTTP_201_CREATED, response_model=PostResponse)
async def create_post_like(post_slug: str, token: token_dependency):
    user = auth_service.get_current_user(token)
    updated_post = post_service.create_post_like(post_slug, user)

    return responses.format_post_response(updated_post)
