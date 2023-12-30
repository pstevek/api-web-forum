import os

from typing import Annotated
from fastapi import Depends
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session, sessionmaker

SQLALCHEMY_DATABASE_URL = "postgresql://{}:{}@{}:5432/{}".format(
    os.environ['DB_USER'],
    os.environ['DB_PASSWORD'],
    os.environ['DB_HOST'],
    os.environ['DB_NAME'],
)

engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


db_dependency = Annotated[Session, Depends(get_db)]


def persist_db(db: db_dependency, model: Base) -> None:
    db.add(model)
    db.commit()
    db.refresh(model)
