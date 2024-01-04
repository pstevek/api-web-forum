import http
import time
from fastapi import Request
from fastapi import FastAPI
from app.api import models
from app.core.database import engine
from app.core.config import settings
from app.core.logger import logger
from app.api.routes.index import api_router
from app.api.middlewares.logging import log_request_middleware
from starlette.middleware.cors import CORSMiddleware

# Database initialization
models.Base.metadata.create_all(bind=engine)

# App initialization
app = FastAPI(
    title=settings.PROJECT_NAME,
    description=settings.PROJECT_DESCRIPTION,
    version="1.0",
)


app.middleware("http")(log_request_middleware)

# Set all CORS enabled origins
if settings.BACKEND_CORS_ORIGINS:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[str(origin) for origin in settings.BACKEND_CORS_ORIGINS],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

app.include_router(api_router, prefix=settings.API_V1_STR)
