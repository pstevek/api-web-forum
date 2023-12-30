import logging
import app.api.models
from fastapi import FastAPI
from app.core.database import engine, Base
from app.core.config import settings
# from routers import auth, home, posts, users

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('barrows-api')

# Database initialization
Base.metadata.create_all(bind=engine)

# description = "Barrows | Forum Management API"

# App initialization
app = FastAPI(
    title=settings.PROJECT_NAME,
    description=settings.PROJECT_DESCRIPTION,
    version="1.0",
)

@app.get("/info")
async def info():
    return {
        "PROJECT_NAME": settings.PROJECT_NAME,
        "ALGORITHM": settings.ALGORITHM,
    }
#
# # Add routes to app context
# app.include_router(prefix="/api/v1", router=home.router)
# app.include_router(prefix="/api/v1", router=auth.router)
# app.include_router(prefix="/api/v1", router=users.router)
# app.include_router(prefix="/api/v1", router=posts.router)
