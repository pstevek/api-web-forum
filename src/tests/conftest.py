import pytest
from fastapi.testclient import TestClient
from app.core.database import test_engine, Base, use_database_session
from app.main import app
from app.core.config import settings
from seeder import tables

test_users: dict = {
    "username": "SeanCarrington",
    "email": "sean@gmail.com",
    "first_name": "Sean",
    "last_name": "Carrington",
    "password": "password_one"
}


@pytest.fixture()
def setup_test_db():
    settings.TEST_MODE = True
    Base.metadata.create_all(bind=test_engine)
    with use_database_session() as session:
        session.bulk_save_objects(objects=tables['roles'])
        session.commit()
    yield
    Base.metadata.drop_all(bind=test_engine)


@pytest.fixture(scope="module")
def client():
    with TestClient(app) as c:
        yield c
