import models
from fastapi import FastAPI
from database import engine

models.Base.metadata.create_all(bind=engine)
app = FastAPI()


@app.get("/api")
async def root():
    return {"message": "Hello World"}