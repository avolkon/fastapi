"""
Настройки приложения через переменные окружения (.env).

Секреты и ключи не хранятся в репозитории — задаются локально.
"""

from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict


def _resolve_env_file() -> Path:
    """Возвращает путь к `.env` в каталоге `project`."""

    return Path(__file__).resolve().parent.parent.parent / ".env"


class Settings(BaseSettings):
    """Центральный объект конфигурации для JWT, SQLite и OpenRouter."""

    model_config = SettingsConfigDict(
        env_file=str(_resolve_env_file()),
        env_file_encoding="utf-8",
        extra="ignore",
    )

    app_name: str = "llm-p"
    env: str = "local"

    jwt_secret: str
    jwt_alg: str = "HS256"
    access_token_expire_minutes: int = 60

    sqlite_path: str = "./app.db"

    openrouter_api_key: str = ""
    openrouter_base_url: str = "https://openrouter.ai/api/v1"
    openrouter_model: str = "stepfun/step-3.5-flash:free"
    openrouter_site_url: str = "https://example.com"
    openrouter_app_name: str = "llm-fastapi-openrouter"

    cors_origins: str = ""

    def cors_origins_list(self) -> list[str]:
        """Список хостов CORS или пусто, если middleware не нужен."""

        if not self.cors_origins.strip():
            return []
        return [o.strip() for o in self.cors_origins.split(",") if o.strip()]


settings = Settings()
