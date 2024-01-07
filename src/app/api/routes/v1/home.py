from fastapi import APIRouter, status

router = APIRouter(tags=["Home / Health"])


@router.get("/", status_code=status.HTTP_200_OK)
async def home():
    return {"message": "Hello World"}
