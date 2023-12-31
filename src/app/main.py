import logging
from fastapi import FastAPI
from app.api import models
from app.core.database import engine
from app.core.config import settings
from starlette.middleware.cors import CORSMiddleware
from app.api.routes import api_router

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('barrows-api')

# Database initialization
models.Base.metadata.create_all(bind=engine)

# App initialization
app = FastAPI(
    title=settings.PROJECT_NAME,
    description=settings.PROJECT_DESCRIPTION,
    version="1.0",
)

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

#
# # Add routes to app context
# app.include_router(prefix="/api/v1", router=home.router)
# app.include_router(prefix="/api/v1", router=auth.router)
# app.include_router(prefix="/api/v1", router=users.router)
# app.include_router(prefix="/api/v1", router=posts.router)
