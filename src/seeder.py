import logging
from sqlalchemy.exc import IntegrityError
from models import Role, User
from database import SessionLocal
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
        )
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
    ]
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

