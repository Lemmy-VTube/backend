from datetime import datetime
from pathlib import Path

from pydantic import Field, SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict

ROOT_DIR = Path(__file__).parent.parent
ENV_FILE = ROOT_DIR / "src" / ".env"
LOGS_DIR = ROOT_DIR / "logs"

now = datetime.now().replace(microsecond=0)
log_filename_time = now.strftime("%Y-%m-%d_%H-%M-%S")


if not ENV_FILE.exists():
    raise FileNotFoundError(f".env file not found at: {ENV_FILE}")

if not LOGS_DIR.exists():
    LOGS_DIR.mkdir(parents=True, exist_ok=True)


class Config(BaseSettings):
    REDIS_URL: SecretStr
    DB_URL: SecretStr

    APP_HOST: str = "127.0.0.1"
    APP_PORT: int = 8000
    APP_RELOAD: bool = False

    PROJECT_VERSION: str = "v1.0.0-latest"
    API_TITLE: str = "Backend Template in FastAPI"
    API_DESCRIPTION: str = (
        "Open-source backend template powered by FastAPI, SQLAlchemy, Redis, "
        "and other modern Python tools. Ideal for production-ready APIs."
    )
    API_VERSIONS: list[dict] = Field(
        default_factory=lambda: [
            {
                "version": "v1",
                "status": "current",
                "release_date": "31.10.2025",
                "description": "Current stable version of the API",
                "changes": []
            }
        ]
    )

    RATELIMIT_MAX_REQUESTS: int = 60
    RATELIMIT_WINDOW_SECONDS: int = 300
    RATELIMIT_BAN_SECONDS: int = 1800

    DEVELOPER_USERNAME: str = "Kitty_Ilnazik"
    GITHUB_URL: str = "https://github.com/kitty-ilnazik/backend-template"

    model_config = SettingsConfigDict(
        env_file=ENV_FILE,
        env_file_encoding="utf-8"
    )


class ConfigLog(BaseSettings):
    LOG_LEVEL: str = "INFO"
    LOG_FORMAT: str = "%(asctime)s - [%(levelname)s] - %(name)s: %(message)s"
    LOG_DATE_FORMAT: str = "%d.%m.%Y %H:%M:%S"
    LOG_FILE: Path = LOGS_DIR / f"app_{log_filename_time}.log"


config = Config()  # type: ignore
config_log = ConfigLog()
