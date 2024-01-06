from fastapi import FastAPI
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from starlette import status
from starlette.exceptions import HTTPException
from starlette.requests import Request
from starlette.responses import JSONResponse
from starlette.middleware.cors import CORSMiddleware
from app.api import models
from app.api.middlewares.logging import log_request_middleware
from app.core.database import engine
from app.core.config import settings
from app.api.routes.index import api_router
from app.core.exception_handlers import (
    request_validation_exception_handler,
    http_exception_handler,
    unhandled_exception_handler
)

# Database schemas initialization
models.Base.metadata.create_all(bind=engine)

# App initialization
app = FastAPI(
    title=settings.PROJECT_NAME,
    description=settings.PROJECT_DESCRIPTION,
    version="1.0",
    debug=settings.DEBUG
)

# Middlewares
app.middleware("http")(log_request_middleware)
app.add_exception_handler(RequestValidationError, request_validation_exception_handler)
# app.add_exception_handler(HTTPException, http_exception_handler)
# app.add_exception_handler(Exception, unhandled_exception_handler)

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
