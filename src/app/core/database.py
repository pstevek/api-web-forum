from typing import Annotated
from fastapi import Depends
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session, sessionmaker, scoped_session
from app.core.config import settings

SQLALCHEMY_DATABASE_URL = "postgresql://{}:{}@{}:5432/{}".format(
    settings.DB_USER,
    settings.DB_PASSWORD,
    settings.DB_HOST,
    settings.DB_NAME,
)

engine = create_engine(SQLALCHEMY_DATABASE_URL)

session_factory = sessionmaker(autocommit=False, autoflush=False, bind=engine)
SessionLocal = scoped_session(session_factory)

Base = declarative_base()


class DatabaseSessionMixin:
    """Database session mixin."""

    def __enter__(self) -> Session:
        self.db = SessionLocal()
        return self.db

    def __exit__(self, exc_type, exc_val, exc_tb):
        try:
            if exc_type is not None:
                self.db.rollback()
        except SQLAlchemyError:
            pass
        finally:
            self.db.close()
            SessionLocal.remove()


def use_database_session():
    return DatabaseSessionMixin()


db_dependency = Annotated[Session, Depends(use_database_session)]


def persist_db(db: db_dependency, model: Base) -> None:
    print("### NEW MODEL ###", model.__dict__)
    db.add(model)
    db.commit()
    db.refresh(model)
