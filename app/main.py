from fastapi import FastAPI

from app.config.settings import Settings
from app.controller.health import create_health_router
from app.service.health import HealthService


def create_app(settings: Settings | None = None) -> FastAPI:
    """Composition root: load configuration and connect the layers."""
    settings = settings if settings is not None else Settings()
    application = FastAPI(
        title=settings.app_name,
        version=settings.app_version,
        description="Базовый каркас Event Ticketing API — лабораторная работа №3.",
    )
    application.state.settings = settings
    health_service = HealthService(
        app_name=settings.app_name,
        version=settings.app_version,
        environment=settings.app_env,
    )
    application.include_router(create_health_router(health_service))
    return application


app = create_app()
