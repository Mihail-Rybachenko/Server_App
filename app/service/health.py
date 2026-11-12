from time import monotonic

from app.domain.health import HealthStatus


class HealthService:
    """Report process liveness without depending on HTTP or a database."""

    def __init__(self, app_name: str, version: str, environment: str) -> None:
        self._app_name = app_name
        self._version = version
        self._environment = environment
        self._started_at = monotonic()

    def get_status(self) -> HealthStatus:
        return HealthStatus(
            status="pass",
            app=self._app_name,
            version=self._version,
            environment=self._environment,
            uptime=round(monotonic() - self._started_at, 3),
        )
