from app.api.services.user import user_service
from app.core.config import settings
from app.api.schemas import UserCreate
from tests.conftest import client


def test_login(setup_test_db):
    payload: dict = {
        "username": "SeanCarrington",
        "email": "sean@gmail.com",
        "first_name": "Sean",
        "last_name": "Carrington",
        "password": "password_one"
    }

    user_service.create_user(UserCreate(**payload))
    remove_keys = ["email", "first_name", "last_name"]
    for key in remove_keys:
        del payload[key]

    response = client.post(
        url=f"{settings.API_V1_STR}/auth/login",
        data=payload,
        headers={'Content-Type': 'application/x-www-form-urlencoded'}
    )

    assert response.status_code == 200
    assert 'access_token' in response.json()
    assert 'token_type' in response.json()


