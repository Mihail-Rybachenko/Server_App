import pytest
from pydantic import ValidationError

from app.config.settings import Settings


@pytest.fixture(autouse=True)
def clean_environment(monkeypatch):
    for name in ("APP_NAME", "APP_VERSION", "APP_ENV", "HTTP_HOST", "HTTP_PORT"):
        monkeypatch.delenv(name, raising=False)


def test_dotenv_and_environment_priority(tmp_path, monkeypatch):
    env_file = tmp_path / ".env"
    env_file.write_text(
        'APP_NAME="Ticketing from file"\nAPP_ENV=test\nHTTP_PORT=8123\n',
        encoding="utf-8",
    )
    monkeypatch.chdir(tmp_path.parent)
    settings = Settings(_env_file=env_file)
    assert settings.app_name == "Ticketing from file"
    assert settings.app_env == "test"
    assert settings.http_port == 8123

    monkeypatch.setenv("HTTP_PORT", "9123")
    assert Settings(_env_file=env_file).http_port == 9123


@pytest.mark.parametrize("port", ["0", "65536", "not-a-number"])
def test_invalid_port_is_rejected(monkeypatch, port):
    monkeypatch.setenv("HTTP_PORT", port)
    with pytest.raises(ValidationError):
        Settings(_env_file=None)
