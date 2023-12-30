from fastapi import APIRouter

from app.api.v1 import home

api_router = APIRouter()

api_router.include_router(router=home.router)
