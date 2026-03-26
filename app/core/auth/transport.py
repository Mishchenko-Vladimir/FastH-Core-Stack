from fastapi_users.authentication import (
    BearerTransport,
    CookieTransport,
)

from core.config import settings


bearer_transport = BearerTransport(tokenUrl=settings.api.bearer_token_url)

cookie_transport = CookieTransport(
    cookie_name="fastapiusersauth",  # Имя куки
    cookie_max_age=settings.site.cookie_max_age,  # Время жизни куки
    cookie_secure=settings.site.cookie_secure,  # HTTPS
    cookie_httponly=True,  # Защита от XSS
    cookie_samesite="lax",  # Защита от CSRF
)
