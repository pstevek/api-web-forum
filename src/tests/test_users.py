from app.core.config import settings
from tests.test_auth import test_login
from tests.conftest import test_users
from fastapi import status


def test_get_auth_user(setup_test_db, client):
    auth_token = test_login(setup_test_db, client)
    response = client.get(
        url=f"{settings.API_V1_STR}/users/me",
        headers={'Authorization': f"Bearer {auth_token}"}
    )

    json_response = response.json()
    assert response.status_code == status.HTTP_200_OK
    assert json_response['email'] == test_users['email']
    assert json_response['first_name'] == test_users['first_name']
    assert json_response['last_name'] == test_users['last_name']
    assert json_response['username'] == test_users['username']
    assert json_response['role'] == 'Regular'

    return json_response
