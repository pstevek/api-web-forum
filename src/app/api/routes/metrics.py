from typing import List
from fastapi import APIRouter
from app.api.schemas import MetricResponse
from app.api.services.post import post_service

router = APIRouter(prefix="/metrics", tags=["App Metrics"])


@router.get("", response_model=List[MetricResponse])
async def get_metrics():
    return post_service.get_app_metrics()
