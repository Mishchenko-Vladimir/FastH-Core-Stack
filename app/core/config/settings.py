from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict

from .prefix.api import ApiPrefix
from .prefix.view import ViewPrefix

from .app import SiteConfig, RunConfig, GunicornConfig
from .auth import AccessToken, AdminConfig, CsrfSettings, RateLimitConfig
from .cache import CacheConfig, RedisConfig
from .external import WebhookConfig, SMTPConfig
from .db import DataBaseConfig
from .logging import LoggingConfig


# ...\FastH-Core-Stack\app\
BASE_DIR = Path(__file__).resolve().parent.parent.parent


class Settings(BaseSettings):
    """Настройка приложения"""

    model_config = SettingsConfigDict(
        env_file=(BASE_DIR / ".env.template", BASE_DIR / ".env"),
        case_sensitive=False,
        env_nested_delimiter="__",
        env_prefix="APP_CONFIG__",
    )
    site: SiteConfig
    csrf: CsrfSettings
    run: RunConfig = RunConfig()
    gunicorn: GunicornConfig = GunicornConfig()
    logging: LoggingConfig = LoggingConfig()
    api: ApiPrefix = ApiPrefix()
    view: ViewPrefix = ViewPrefix()
    db: DataBaseConfig
    access_token: AccessToken
    webhook: WebhookConfig
    admin: AdminConfig
    rate_limit: RateLimitConfig
    redis: RedisConfig = RedisConfig()
    cache: CacheConfig
    smtp: SMTPConfig


settings = Settings()  # type: ignore
