from app.api.services.user import user_service
from app.core.config import settings
from app.api.schemas import UserCreate
from tests.conftest import test_users
from fastapi import status


def test_login(setup_test_db, client):
    payload = test_users.copy()
    user_service.create_user(UserCreate(**payload))
    remove_keys = ["email", "first_name", "last_name"]
    for key in remove_keys:
        del payload[key]

    response = client.post(
        url=f"{settings.API_V1_STR}/auth/login",
        data=payload,
        headers={'Content-Type': 'application/x-www-form-urlencoded'}
    )

    json_response = response.json()
    assert response.status_code == status.HTTP_200_OK
    assert 'access_token' in json_response
    assert 'token_type' in json_response

    return json_response['access_token']


def test_register(setup_test_db, client):
    payload = test_users.copy()
    print("### payload ###", payload)
    response = client.post(
        url=f"{settings.API_V1_STR}/auth/register",
        json=payload
    )
    json_response = response.json()
    assert response.status_code == status.HTTP_201_CREATED
    assert isinstance((json_response['id']), int)
    assert json_response['email'] == payload['email']
    assert json_response['first_name'] == payload['first_name']
    assert json_response['last_name'] == payload['last_name']
    assert json_response['username'] == payload['username']
    assert json_response['role'] == 'Regular'
