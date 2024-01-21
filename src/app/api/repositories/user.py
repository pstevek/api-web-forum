from app.api.repositories.base import BaseRepository
from app.api.models import User
from app.api.schemas import UserCreate, UserUpdate
from app.api.dependencies import pwd_context
from sqlalchemy.orm import joinedload
from sqlalchemy import and_


class UserRepository(BaseRepository):
    model = User

    def get_by_username(self, username: str) -> User:
        return self.db.query(self.model).options(joinedload(User.role)).filter(
            and_(
                User.username == username,
                User.deleted_at.is_(None)
            )
        ).first()

    def create(self, user_request: UserCreate) -> User:
        new_user = User(
            email=user_request.email,
            username=user_request.username,
            first_name=user_request.first_name,
            last_name=user_request.last_name,
            role_id=2,
            password=pwd_context.hash(user_request.password),
        )

        return super().create(object_in=new_user)

    def update(self, user_request: UserUpdate, user: User) -> User:
        update_data = user_request if isinstance(user_request, dict) else user_request.dict(exclude_unset=True)

        if update_data.get("password"):
            update_data["password"] = pwd_context.hash(update_data["password"])

        return super().update(db_obj=user, object_in=update_data)

    @staticmethod
    def is_admin(user: User) -> bool:
        return user.role.slug == 'moderator'


user_repository = UserRepository()
