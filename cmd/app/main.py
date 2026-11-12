from pathlib import Path
import sys

# Позволяет запускать файл напрямую: python cmd/app/main.py.
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

import uvicorn
from fastapi import FastAPI

from internal.config.settings import Settings
from internal.controller.health import create_health_router
from internal.service.health import HealthService


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


if __name__ == "__main__":
    settings = app.state.settings
    uvicorn.run(app, host=settings.http_host, port=settings.http_port)
