import asyncio

import httpx

from app.config.settings import Settings
from app.main import create_app


def test_health_is_public_and_uses_configuration():
    settings = Settings(
        _env_file=None,
        app_name="Ticketing Test",
        app_version="2.0.0",
        app_env="test",
    )

    async def check_response():
        transport = httpx.ASGITransport(app=create_app(settings))
        async with httpx.AsyncClient(transport=transport, base_url="http://test") as client:
            response = await client.get("/api/v1/health")
            assert response.status_code == 200
            assert response.headers["content-type"] == "application/json"
            payload = response.json()
            assert payload == {
                "status": "pass",
                "app": "Ticketing Test",
                "version": "2.0.0",
                "environment": "test",
                "uptime": payload["uptime"],
            }
            assert isinstance(payload["uptime"], (int, float))
            assert payload["uptime"] >= 0
            next_response = await client.get("/api/v1/health")
            assert next_response.json()["uptime"] >= payload["uptime"]

    asyncio.run(check_response())
