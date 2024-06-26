from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from redis import asyncio as aioredis
from fastapi import FastAPI
from pydantic import ValidationError
from fastapi.exceptions import RequestValidationError
from starlette.middleware.cors import CORSMiddleware
from app.api.middlewares.logging import log_request_middleware
from app.core.config import settings
from app.api.routes.index import api_router
from app.api.routes.metrics import router as metrics_router
from app.core.exception_handlers import (
    request_validation_exception_handler,
    pydantic_validation_exception_handler,
)


# App initialization
app = FastAPI(
    title=settings.PROJECT_NAME,
    description=settings.PROJECT_DESCRIPTION,
    version="1.0",
    debug=settings.DEBUG,
    docs_url='/api/docs'
)

# Middlewares
app.middleware("http")(log_request_middleware)
app.add_exception_handler(RequestValidationError, request_validation_exception_handler)
app.add_exception_handler(ValidationError, pydantic_validation_exception_handler)


# Set all CORS enabled origins
if settings.BACKEND_CORS_ORIGINS:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[str(origin) for origin in settings.BACKEND_CORS_ORIGINS],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )


# Cache init
@app.on_event("startup")
async def startup():
    redis = aioredis.from_url(url=settings.REDIS_URL)
    FastAPICache.init(RedisBackend(redis), prefix="fastapi-cache")

# Load routes
app.include_router(api_router, prefix=settings.API_V1_STR)
app.include_router(metrics_router)
