from fastapi import APIRouter, status

router = APIRouter(tags=["Home / Health"])


@router.get("/")
async def home(status_code=status.HTTP_200_OK):
    return {"message": "Hello World"}
