import logging
import httpx
import random
from sqlalchemy.exc import IntegrityError
from app.api.models import Role, User, Post, Like
from app.core.database import SessionLocal
from app.core.config import settings
from slugify import slugify
from datetime import datetime
from passlib.context import CryptContext


pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')

tables = {
    'users': [
        User(
            email="admin@gmail.com",
            first_name="Admin",
            last_name="User",
            username="admin",
            password=pwd_context.hash("admin"),
            role_id=1,
            created_at=datetime.now(),
        ),
        User(
            email="steve.kamanke@gmail.com",
            first_name="Steve",
            last_name="Kamanke",
            username="pstevek",
            password=pwd_context.hash('password'),
            role_id=2,
            created_at=datetime.now(),
        ),
        User(
            email="user@barrows.co.za",
            first_name="Test",
            last_name="User",
            username="user.barrows",
            password=pwd_context.hash('password'),
            role_id=2,
            created_at=datetime.now(),
        ),
    ],

    'roles': [
        Role(
            slug="moderator",
            name="Moderator",
            created_at=datetime.now()
        ),
        Role(
            slug="regular",
            name="Regular",
            created_at=datetime.now()
        )
    ],

    'likes': [
        Like(
            user_id=2,
            post_id=1
        ),
        Like(
            user_id=3,
            post_id=1
        )
    ],

    'posts': []
}


def run_seeder(table: str) -> None:
    if table not in list(tables):
        raise ValueError("Seeder Table not found")

    try:
        session = SessionLocal()
        session.bulk_save_objects(objects=tables[table])
        session.commit()
    except IntegrityError:
        logging.error("Duplicate transaction detected. Seeder likely ran already")


if __name__ == "__main__":
    _api_posts_endpoint = settings.SAMPLE_POST_API
    try:
        response = httpx.get(_api_posts_endpoint)
        response.raise_for_status()
        blogs = response.json()['blogs']
        for i in range(0, 10):
            tables['posts'].append(
                Post(
                    user_id=random.randint(2, 3),
                    title=blogs[i]['title'],
                    slug=slugify(blogs[i]['title']),
                    content=blogs[i]['content_html']
                )
            )
    except httpx.RequestError as exc:
        print(f"An error occurred while requesting {exc.request.url!r}.")
    except httpx.HTTPStatusError as exc:
        print(f"Error response {exc.response.status_code} while requesting {exc.request.url!r}.")

    run_seeder("roles")
    run_seeder("users")
    run_seeder("posts")
    run_seeder("likes")
