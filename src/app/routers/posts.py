import traceback

from typing import Annotated
from routers.auth import get_current_user
from fastapi import APIRouter, Depends, HTTPException, status
from models import Post, Comment, Like
from database import db_dependency, persist_db
from schemas import CommentCreate, PostResponse, UserResponse
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import joinedload, Session
from sqlalchemy import and_

router = APIRouter(prefix="/posts", tags=["Post Management"])
authenticated_user = Annotated[UserResponse, Depends(get_current_user)]


def get_single_post(post_id: int, db: Session = Depends(db_dependency)) -> Post:
    post = db.query(Post)\
        .options(joinedload('comments'))\
        .options(joinedload('likes'))\
        .filter(
            and_(
                Post.id == post_id,
                Post.deleted_at.is_(None)
            )
        ).first()

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")

    return post


@router.get("", response_model=list[PostResponse])
def get_all_posts(db: db_dependency, skip: int = 0, limit: int = 100):
    posts = db.query(Post)\
        .options(joinedload('comments'))\
        .options(joinedload('likes'))\
        .filter(Post.deleted_at.is_(None))\
        .order_by(Post.created_at.desc())\
        .offset(skip)\
        .limit(limit)\
        .all()

    return list(posts)


@router.get("/{post_id}", response_model=PostResponse)
def get_post(post_id: int, db: db_dependency):
    return get_single_post(post_id, db)


@router.post("/{post_id}/comments", status_code=status.HTTP_201_CREATED)
def create_post_comment(user: authenticated_user, post_id: int, request: CommentCreate, db: db_dependency):
    post = get_single_post(post_id, db)

    try:
        comment = Comment(
            post_id=post_id,
            user_id=user.id,
            content=request.content
        )

        post.comments.append(comment)

        persist_db(db, post)

        return PostResponse(**jsonable_encoder(post))
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error occurred while performing request :: {traceback.format_exc()}"
        )


@router.post("/{post_id}/like", status_code=status.HTTP_201_CREATED)
def like_post(user: authenticated_user, post_id: int, db: db_dependency):
    post = get_single_post(post_id, db)

    try:
        like = Like(
            post_id=post_id,
            user_id=user.id
        )

        post.likes.append(like)

        persist_db(db, post)

        return PostResponse(**jsonable_encoder(post))
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error occurred while performing request :: {traceback.format_exc()}"
        )


@router.get("/{post_id}/likes", status_code=status.HTTP_200_OK)
def get_post_likes(post_id: int, db: db_dependency):
    post = get_single_post(post_id, db)

    return [{"user": like.user.full_name()} for like in post.likes]
