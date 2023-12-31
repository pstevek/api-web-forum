from app.api.repositories.base import BaseRepository
from app.core.database import persist_db, use_database_session
from app.api.models import User
from app.api.schemas import UserCreate, UserUpdate
from app.api.dependencies import pwd_context
from fastapi import status, HTTPException


class UserRepository(BaseRepository):
    def get(self, user_id: int) -> User | HTTPException:
        user = super().get(model_id=user_id)

        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

        return user

    def get_by_username(self, username: str) -> User | HTTPException:
        user = self.db.query(User).filter(User.username == username).first()

        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

        return user

    def create(self, user_request: UserCreate) -> User:
        new_user = User(
            email=user_request.email,
            username=user_request.username,
            first_name=user_request.first_name,
            last_name=user_request.last_name,
            role_id=2,
            password=pwd_context.hash(user_request.password),
        )

        persist_db(self.db, new_user)

        return new_user

    def update(self, user_request: UserUpdate, user: User) -> User:
        update_data = user_request if isinstance(user_request, dict) else user_request.dict(exclude_unset=True)

        if update_data.get("password"):
            update_data["password"] = pwd_context.hash(user_request["password"])

        return super().update(db_obj=user, object_in=update_data)


with use_database_session() as session:
    user_repository = UserRepository(model=User, db=session)

