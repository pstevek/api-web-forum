from typing import List

from app.api.models import User, Post, Like, Comment
from app.api.schemas import UserResponse, PostResponse, TokenResponse, LikeResponse, CommentResponse
from fastapi.encoders import jsonable_encoder


def format_user_response(user: User) -> UserResponse:
    response = jsonable_encoder(user)
    response['role'] = user.role.name

    return UserResponse(**response)


def format_comment(comment: Comment) -> CommentResponse:
    response = jsonable_encoder(comment)
    response['user'] = comment.user.full_name()
    response['post_slug'] = comment.post.slug

    return CommentResponse(**response)


def format_like(like: Like) -> LikeResponse:
    response = jsonable_encoder(like)
    response['user'] = like.user.full_name()
    response['post_slug'] = like.post.slug

    return LikeResponse(**response)


def format_post_response(post: Post) -> PostResponse:
    response = jsonable_encoder(post)
    response['user'] = post.user.full_name()

    post_likes = post.likes
    post_comments = post.comments

    if post_likes:
        response['likes'] = [format_like(like) for like in post_likes]
    if post_comments:
        response['comments'] = [format_comment(comment) for comment in post_comments]

    return PostResponse(**response)


def format_posts_response(posts: List[Post]) -> List[PostResponse]:
    return [format_post_response(post) for post in posts]


def format_token_response(token: str) -> TokenResponse:
    return TokenResponse(**{"access_token": token})
