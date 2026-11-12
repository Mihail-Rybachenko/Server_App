from dataclasses import asdict
from typing import Literal

from fastapi import APIRouter
from pydantic import BaseModel, Field

from internal.service.health import HealthService


class HealthResponse(BaseModel):
    status: Literal["pass"]
    app: str
    version: str
    environment: str
    uptime: float = Field(ge=0, description="Время работы приложения в секундах")


def create_health_router(service: HealthService) -> APIRouter:
    router = APIRouter(prefix="/api/v1", tags=["Health"])

    @router.get(
        "/health",
        response_model=HealthResponse,
        summary="Проверка работоспособности сервиса",
    )
    def health() -> HealthResponse:
        return HealthResponse(**asdict(service.get_status()))

    return router
