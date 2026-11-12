from dataclasses import dataclass
from time import monotonic
from typing import Literal


@dataclass(frozen=True)
class HealthStatus:
    status: Literal["pass"]
    app: str
    version: str
    environment: str
    uptime: float


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
