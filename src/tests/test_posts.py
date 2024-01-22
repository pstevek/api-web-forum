from fastapi import status
from app.core.config import settings
from app.api.services.post import post_service
from app.api.services.user import user_service
from app.api.schemas import UserCreate, PostCreate


def test_get_user_posts(setup_test_db, client):
    post_number = 4
    user_details = {
        "username": "SeanCarrington",
        "email": "sean@gmail.com",
        "first_name": "Sean",
        "last_name": "Carrington",
        "password": "password_one"
    }
    user = user_service.create_user(UserCreate(**user_details))

    for i in range(post_number):
        post_details = {
            "title": f"Demo Title Post #{i}",
            "content": f"Demo Content Post #{i}"
        }
        post_service.create_user_post(user, PostCreate(**post_details))

    response = client.get(url=f"{settings.API_V1_STR}/posts")

    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()) == post_number


