from typing import List
from app.api.models import Post, Comment, Like
from app.api.repositories.base import BaseRepository
from app.api.schemas import PostCreate, CommentCreate
from app.core.database import use_database_session, persist_db
from sqlalchemy import and_, desc, func, extract
from slugify import slugify
from datetime import timedelta


class PostRepository(BaseRepository):
    model = Post

    def get_all_posts(
            self,
            query: str | None = None,
            skip: int = 0,
            limit: int = 10,
            joint_tables: list | None = None
    ) -> List[model]:
        orderby = None
        filtered = self.model.deleted_at.is_(None)
        if query is not None:
            filtered = and_(
                filtered,
                self.model.content.contains(query)
            )
            orderby = desc(
                func.length(self.model.content) - func.length(func.replace(self.model.content, query, ""))
            )

        return super().all(
            skip=skip, limit=limit, filtered=filtered, orderby=orderby, joint_tables=joint_tables
        )

    def get_post_by_slug(self, slug: str, joint_tables=None) -> model:
        query = self.db.query(self.model)
        query = self.add_joint_tables(query, joint_tables)

        return query.filter(
            and_(
                self.model.slug == slug,
                self.model.deleted_at.is_(None)
            )
        ).first()

    def get_user_posts(self, user_id: int, skip: int = 0, limit: int = 10) -> List[model]:
        return self.db.query(self.model).filter(
            and_(
                self.model.user_id == user_id,
                self.model.deleted_at.is_(None)
            )
        ).offset(skip).limit(limit).all()

    def create_user_post(self, user_id: int, request: PostCreate) -> model:
        new_post = Post(
            user_id=user_id,
            title=request.title,
            content=request.content,
            slug=slugify(request.title)
        )

        return super().create(object_in=new_post)

    def create_post_comment(self, user_id: int, post: model, request: CommentCreate) -> model:
        comment = Comment(
            post_id=post.id,
            user_id=user_id,
            content=request.content
        )

        post.comments.append(comment)
        persist_db(self.db, post)

        return post

    def create_post_like(self, user_id: int, post: model) -> model:
        like = Like(
            post_id=post.id,
            user_id=user_id
        )

        post.likes.append(like)
        persist_db(self.db, post)

        return post

    def app_metrics(self):
        now = func.now()
        start_time = now - timedelta(days=1)

        return self.db.query(
            extract("hour", self.model.created_at).label("hour"),
            func.count(self.model.id).label("post_count"),
            func.count(Comment.id).label("comment_count"),
        ).filter(
            self.model.created_at >= start_time
        ).outerjoin(
            Comment, Comment.post_id == self.model.id
        ).order_by("hour").group_by("hour").all()


with use_database_session() as session:
    post_repository = PostRepository(db=session)
