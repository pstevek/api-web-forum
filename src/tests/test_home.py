from fastapi import status
from tests.conftest import client
from app.core.config import settings


def test_home(client):
    response = client.get(
        url=settings.API_V1_STR
    )

    json_response = response.json()
    assert response.status_code == status.HTTP_200_OK
    assert 'message' in json_response
    assert json_response['message'] == 'Hello World'
