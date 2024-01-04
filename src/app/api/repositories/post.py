from typing import List
from app.api.models import Post, Comment, Like
from app.api.repositories.base import BaseRepository
from app.api.schemas import PostCreate, CommentCreate
from app.core.database import use_database_session, persist_db
from sqlalchemy import and_
from slugify import slugify


class PostRepository(BaseRepository):
    model = Post

    def get_post_by_slug(self, slug: str, joint_tables=None) -> Post:
        query = self.db.query(self.model)
        query = self.add_joint_tables(query, joint_tables)

        return query.filter(
            and_(
                self.model.slug == slug,
                self.model.deleted_at.is_(None)
            )
        ).first()

    def get_user_posts(self, user_id: int, skip: int = 0, limit: int = 100) -> List[Post]:
        return self.db.query(self.model).filter(
            and_(
                self.model.user_id == user_id,
                self.model.deleted_at.is_(None)
            )
        ).offset(skip).limit(limit).all()

    def create_user_post(self, user_id: int, request: PostCreate) -> Post:
        new_post = Post(
            user_id=user_id,
            title=request.title,
            content=request.content,
            slug=slugify(request.title)
        )

        return super().create(object_in=new_post)

    def create_post_comment(self, user_id: int, post: Post, request: CommentCreate) -> Post:
        comment = Comment(
            post_id=post.id,
            user_id=user_id,
            content=request.content
        )

        post.comments.append(comment)
        persist_db(self.db, post)

        return post

    def create_post_like(self, user_id: int, post: Post) -> Post:
        like = Like(
            post_id=post.id,
            user_id=user_id
        )

        post.likes.append(like)
        persist_db(self.db, post)

        return post


with use_database_session() as session:
    post_repository = PostRepository(db=session)
