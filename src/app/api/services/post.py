import traceback
from app.api.services.user import user_service
from app.api.models import Post, User
from app.api.repositories.post import post_repository
from app.api.schemas import PostCreate, PostUpdate, CommentCreate
from fastapi.encoders import jsonable_encoder
from fastapi import HTTPException
from starlette import status


class PostService:
    def __init__(self):
        self.repository = post_repository
        self.tables = ["comments", "likes", "user"]

    def get_all_posts(self, skip: int = 0, limit: int = 100, query: str | None = None):
        try:
            return self.repository.all(skip, limit, query, joint_tables=self.tables)
        except Exception:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error occurred while performing request :: {traceback.format_exc()}"
            )

    def get_post_by_id(self, post_id: int) -> Post | HTTPException:
        try:
            post = self.repository.get(model_id=post_id, joint_tables=self.tables)
        except Exception:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error occurred while performing request :: {traceback.format_exc()}"
            )

        if post is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")

        return post

    def get_post_by_slug(self, slug: str) -> Post | HTTPException:
        try:
            post = self.repository.get_post_by_slug(slug=slug, joint_tables=self.tables)
        except Exception:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error occurred while performing request :: {traceback.format_exc()}"
            )

        if post is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")

        return post

    def create_user_post(self, user: User, request: PostCreate) -> Post | HTTPException:
        try:
            return self.repository.create_user_post(user_id=user.id, request=request)
        except Exception:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error occurred while performing request :: {traceback.format_exc()}"
            )

    def create_post_comment(self, post_slug: str, user: User, request: CommentCreate) -> Post:
        post = self.get_post_by_slug(post_slug)

        try:
            return self.repository.create_post_comment(user_id=user.id, post=post, request=request)
        except Exception:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error occurred while performing request :: {traceback.format_exc()}"
            )

    def create_post_like(self, post_slug: str, user: User) -> Post:
        post = self.get_post_by_slug(post_slug)

        if user.id in [like['user_id'] for like in jsonable_encoder(post.likes)]:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Like already submitted"
            )

        try:
            return self.repository.create_post_like(user_id=user.id, post=post)
        except Exception:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error occurred while performing request :: {traceback.format_exc()}"
            )

    def update_post(self, post_slug: str, user: User, request: PostUpdate) -> Post:
        if not user_service.is_admin(user):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You do not have permission to perform this operation"
            )

        post = self.get_post_by_slug(post_slug)

        try:
            return self.repository.update(post, request)
        except Exception:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error occurred while performing request :: {traceback.format_exc()}"
            )


post_service = PostService()
