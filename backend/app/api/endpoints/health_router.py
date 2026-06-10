from fastapi import APIRouter, Depends, HTTPException
from loguru import logger

from app.core.dependencies import get_health_service
from app.schemas.response import CommonResponse

from app.services.health_service import HealthService
from app.schemas.health import HealthRequest


api_router = APIRouter(tags=["health"])

@api_router.get("/health")
async def health():
    return CommonResponse.ok({"status": "ok"})

@api_router.get("/error")
async def error():
    return CommonResponse.error("Test Error")
    # raise ValueError("Test Error")
    # raise HTTPException(status_code=400, detail="Test Error")


@api_router.post("/health/database")
async def health_check(
    payload: HealthRequest,
    healthz_service: HealthService = Depends(get_health_service),
):
    result = await healthz_service.health_check(payload)
    return CommonResponse.ok(result)

    