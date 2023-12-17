from sqlalchemy import Column, DateTime, String, Integer, ForeignKey, Boolean
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from database import Base

class BaseModel(Base):
    id = Column(Integer, primary_key=True, index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    deleted_at = Column(DateTime(timezone=True), onupdate=func.now())

class Role(BaseModel):
    __tablename__ = "roles"

    slug = Column(String, unique=True, index=True)
    name = Column(String)

    user = relationship("User", back_populates="role", uselist=False)

class User(BaseModel):
    __tablename__ = "users"

    role_id = Column(Integer, ForeignKey("roles.id"))
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    first_name = Column(String)
    last_name = Column(String)
    hashed_password = Column(String)

    role = relationship("Role", back_populates="user")
    posts = relationship("Post", back_populates="user")
    likes = relationship("Like", back_populates="user")

class Post(BaseModel):
    __tablename__ = "posts"

    user_id = Column(Integer, ForeignKey("users.id"))
    title = Column(String)
    content = Column(String)
    is_misleading = Column(Boolean, default=False)

    comments = relationship("Comment", back_populates="post")
    likes = relationship("Like", back_populates="post")
    user = relationship("User", back_populates="posts")


class Comment(BaseModel):
    __tablename__ = "comments"

    user_id = Column(Integer, ForeignKey("users.id"))
    post_id = Column(Integer, ForeignKey("posts.id"))
    content = Column(String)

    user = relationship("User", back_populates="comments")
    post = relationship("Post", back_populates="comments")

class Like(BaseModel):
    __tablename__ = "likes"

    user_id = Column(Integer, ForeignKey("users.id"))
    post_id = Column(Integer, ForeignKey("posts.id"))
    content = Column(String)

    user = relationship("User", back_populates="likes")
    post = relationship("Post", back_populates="likes")

