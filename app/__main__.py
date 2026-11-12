"""Run from the project root: python -m app."""

import uvicorn

from app.main import app


if __name__ == "__main__":
    settings = app.state.settings
    uvicorn.run(app, host=settings.http_host, port=settings.http_port)
