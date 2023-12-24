import traceback
from datetime import datetime

from typing import Annotated
from fastapi import APIRouter, HTTPException, Depends, status
from models import Post, User
from database import db_dependency, persist_db
from schemas import PostCreate, PostUpdate, PostResponse, UserResponse
from starlette import status
from starlette.responses import JSONResponse
from slugify import slugify
from fastapi.encoders import jsonable_encoder
from routers.auth import get_current_user
from sqlalchemy import and_


router = APIRouter(prefix="/users", tags=["User Management"])
authenticated_user = Annotated[UserResponse, Depends(get_current_user)]


@router.get("/{user_id}/posts", response_model=list[PostResponse])
def get_user_posts(user_id: int, db: db_dependency, skip: int = 0, limit: int = 100):
    try:
        posts = db.query(Post).filter(
            and_(
                Post.user_id == user_id,
                Post.deleted_at.is_(None)
            )
        ).offset(skip).limit(limit).all()

        return jsonable_encoder(posts)
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error occurred while performing request :: {traceback.format_exc()}"
        )


@router.post("/{user_id}/posts", status_code=status.HTTP_201_CREATED)
def create_user_post(user_id: int, request: PostCreate, user: authenticated_user, db: db_dependency):
    if user_id != user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to create post")
    try:
        new_post = Post(
            user_id=user_id,
            title=request.title,
            content=request.content,
            slug=slugify(request.title)
        )

        persist_db(db, new_post)

        return JSONResponse(
            content={"message": "Post created successfully"},
            status_code=status.HTTP_201_CREATED
        )
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error occurred while performing request :: {traceback.format_exc()}"
        )


@router.put("/{user_id}/posts/{post_id}", response_model=PostResponse, status_code=status.HTTP_200_OK)
def update_user_post(user_id: int, post_id: int, request: PostUpdate, user: authenticated_user, db: db_dependency):
    if user_id != user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to update post")

    post = db.query(Post).filter(
        and_(
            Post.id == post_id,
            Post.user_id == user_id
        )
    ).first()

    if post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")

    if request.title:
        post.title = request.title
        post.slug = slugify(request.title)
    if request.content:
        post.content = request.content

    try:
        persist_db(db, post)

        return PostResponse(**jsonable_encoder(post))
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error occurred while performing request :: {traceback.format_exc()}"
        )


@router.delete("/{user_id}/posts/{post_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user_post(user_id: int, post_id: int, user: authenticated_user, db: db_dependency):
    if user_id != user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to delete post")

    post = db.query(Post).filter(
        and_(
            Post.id == post_id,
            Post.user_id == user_id
        )
    ).first()

    if post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")

    try:
        post.deleted_at = datetime.now()
        persist_db(db, post)
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error occurred while performing request :: {traceback.format_exc()}"
        )
