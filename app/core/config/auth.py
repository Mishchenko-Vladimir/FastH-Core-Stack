from typing import Literal
from pydantic import BaseModel, SecretStr


class AccessToken(BaseModel):
    """Настройки токена"""

    # Срок жизни токена
    lifetime_seconds: int = 3600

    reset_password_token_secret: SecretStr
    verification_token_secret: SecretStr


class AdminConfig(BaseModel):
    """Конфигурация администратора"""

    # True - Публичная форма аутентификации для администратора
    # False - SQLAdmin форма аутентификации
    use_public_admin_auth: bool = True
    admin_panel_url: str = "/admin-panel"

    admin_email: str
    admin_password: SecretStr
    secret_key: SecretStr


class CsrfSettings(BaseModel):
    """Настройки защиты от CSRF"""

    secret_key: str
    cookie_max_age: int = 3600
    cookie_key: str = "fastapi_csrf"
    token_key: str = "csrf_token"
    cookie_samesite: str = "lax"
    token_location: Literal["body", "header"] = "body"
    methods: set = {"POST", "PUT", "PATCH", "DELETE"}
    cookie_secure: bool = False  # будет установлено из SiteConfig в core.auth.transport.py


class RateLimitConfig(BaseModel):
    """Конфигурация ограничения частоты запросов (rate limiting)"""

    enabled: bool = True
    default_limits: list[str] = ["40/minute"]