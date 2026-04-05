import logging

from typing import Literal
from pathlib import Path
from pydantic import BaseModel, PostgresDsn
from pydantic_settings import BaseSettings, SettingsConfigDict

# Получаем путь до корневой директории проекта
# ...\fastapi-boilerplate\app\
BASE_DIR = Path(__file__).resolve().parent.parent

# Формат логирования
LOG_DEFAULT_FORMAT = (
    "[%(asctime)s.%(msecs)03d] %(module)10s:%(lineno)-3d %(levelname)-7s - %(message)s"
)


class SiteConfig(BaseModel):
    """Конфигурация сайта — домен, протокол, название, базовые URL"""

    site_name: str
    domain: str
    protocol: str = "https"
    environment: Literal["development", "testing", "staging", "production"] = (
        "development"
    )

    # Настройки куки
    cookie_max_age: int = 3600  # время жизни куки в секундах
    cookie_secure: bool = False  # будет установлено через .model_post_init()

    # Список разрешенных доменов для кросс-доменных запросов (сайты с которых можно отправлять запросы на наш API)
    allowed_origins: list[str] = [
        "http://localhost:8000",
        "http://127.0.0.1:8000",
        "http://localhost:1080",
        "http://localhost:1025",
    ]

    @property
    def base_url(self) -> str:
        return f"{self.protocol}://{self.domain}"

    def model_post_init(self, __context) -> None:
        """Установка cookie_secure на основе окружения"""
        if self.environment == "production":
            self.cookie_secure = True
        else:
            self.cookie_secure = False


class RunConfig(BaseModel):
    """Конфигурация запуска"""

    host: str = "127.0.0.1"
    port: int = 8000


class GunicornConfig(BaseModel):
    """Конфигурация запуска через gunicorn"""

    host: str = "0.0.0.0"
    port: int = 8000
    workers: int = 1
    timeout: int = 900


class LoggingConfig(BaseModel):
    """Конфигурация логирования"""

    log_level: Literal[
        "debug",
        "info",
        "warning",
        "error",
        "critical",
    ] = "info"
    log_format: str = LOG_DEFAULT_FORMAT

    @property
    def log_level_value(self) -> int:
        return logging.getLevelNamesMapping()[self.log_level.upper()]


class ViewPrefix(BaseModel):
    """Конфигурация префикса для страниц"""

    home: str = ""
    page_missing: str = "/page-missing"
    limit_exceeded: str = "/limit-exceeded"
    auth: str = "/auth"


class ApiV1Prefix(BaseModel):
    """Конфигурация префикса API версии 1"""

    prefix: str = "/v1"
    webhooks: str = "/webhooks"
    auth: str = "/auth"
    users: str = "/users"


class ApiPrefix(BaseModel):
    """Конфигурация префикса API"""

    prefix: str = "/api"
    v1: ApiV1Prefix = ApiV1Prefix()

    @property
    def bearer_token_url(self) -> str:
        # api/v1/auth/login
        parts = (self.prefix, self.v1.prefix, self.v1.auth, "/login")
        path = "".join(parts)
        return path.removeprefix("/")  # Удаляем начальный /


class DataBaseConfig(BaseModel):
    """Подключение к базе данных"""

    url: PostgresDsn
    echo: bool = False
    echo_pool: bool = False
    pool_size: int = 50
    max_overflow: int = 10

    naming_convention: dict[str, str] = {
        "ix": "ix_%(column_0_label)s",
        "uq": "uq_%(table_name)s_%(column_0_N_name)s",
        "ck": "ck_%(table_name)s_%(constraint_name)s",
        "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
        "pk": "pk_%(table_name)s",
    }


class WebhookConfig(BaseModel):
    """Конфигурация вебхука, для отправки сообщений"""

    # Куда будут отправляться сообщения
    webhook_url: str


class AdminConfig(BaseModel):
    """Конфигурация администратора"""

    # True - Публичная форма аутентификации для администратора
    # False - SQLAdmin форма аутентификации
    public_auth: bool = True
    admin_panel_url: str = "/admin-panel"

    admin_email: str
    admin_password: str


class RateLimitConfig(BaseModel):
    """Конфигурация ограничения частоты запросов (rate limiting)"""

    enabled: bool = True
    default_limits: list[str] = ["40/minute"]


class AccessToken(BaseModel):
    """Настройки токена"""

    # Срок жизни токена
    lifetime_seconds: int = 3600

    reset_password_token_secret: str
    verification_token_secret: str


class RedisDB(BaseModel):
    """Настройки Redis"""

    cache: int = 0


class RedisConfig(BaseModel):
    """Настройки Redis"""

    host: str = "localhost"
    port: int = 6379
    db: RedisDB = RedisDB()


class CacheNamespace(BaseModel):
    """Именование пространства кэша"""

    users_list: str = "users-list"


class CacheConfig(BaseModel):
    """Настройки кэша"""

    enabled: bool = True
    prefix: str = "fastapi-cache"
    namespace: CacheNamespace = CacheNamespace()


class SMTPConfig(BaseModel):
    """Конфигурация SMTP для отправки писем"""

    # Режим работы приложения: False - письма уходили в MailHog, True - отправляются на реальный SMTP
    enabled: bool = False

    host: str  # SMTP-сервер (smtp.gmail.com, smtp.yandex.ru, smtp.mail.ru, smtp-mail.outlook.com , smtp.sendgrid.net)
    port: int = 587  # Порт для подключения: 587 (TLS), 465 (SSL), 25 (устаревший)
    username: str  # Логин (обычно email)
    password: str  # (app password - пароль для приложения)
    use_tls: bool = True  # Использовать ли шифрование TLS
    timeout: int = 10  # Максимальное время ожидания ответа от сервера (в секундах)


class Settings(BaseSettings):
    """Настройка приложения"""

    model_config = SettingsConfigDict(
        env_file=(BASE_DIR / ".env.template", BASE_DIR / ".env"),
        case_sensitive=False,
        env_nested_delimiter="__",
        env_prefix="APP_CONFIG__",
    )
    site: SiteConfig
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
