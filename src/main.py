import models
import logging
from fastapi import FastAPI
from database import engine
from routers import auth, home, posts, users

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('barrows-api')

# Database initialization
models.Base.metadata.create_all(bind=engine)

description = "Barrows | Forum Management API"

# App initialization
app = FastAPI(
    title="Barrows API",
    description=description, version="1.0",
)

# Add routes to app context
app.include_router(prefix="/api/v1", router=home.router)
app.include_router(prefix="/api/v1", router=auth.router)
app.include_router(prefix="/api/v1", router=users.router)
app.include_router(prefix="/api/v1", router=posts.router)
