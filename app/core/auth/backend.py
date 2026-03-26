from fastapi_users.authentication import AuthenticationBackend

from .transport import (
    # bearer_transport,
    cookie_transport,
)
from .strategy import get_database_strategy


# Используется в FastAPI Users для защиты маршрутов (можно выбрать bearer или cookie).
authentication_backend = AuthenticationBackend(
    name="access-token-db",
    # transport=bearer_transport,
    transport=cookie_transport,
    get_strategy=get_database_strategy,  # Хранение токенов в БД
)
