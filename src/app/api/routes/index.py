from fastapi import APIRouter

from app.api.routes.v1 import home, auth, users

api_router = APIRouter()

api_router.include_router(router=home.router)
api_router.include_router(router=auth.router)
api_router.include_router(router=users.router)
