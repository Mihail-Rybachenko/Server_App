from dataclasses import dataclass
from typing import Literal


@dataclass(frozen=True)
class HealthStatus:
    status: Literal["pass"]
    app: str
    version: str
    environment: str
    uptime: float
