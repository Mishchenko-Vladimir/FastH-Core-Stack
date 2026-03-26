from typing import TYPE_CHECKING, Annotated
from fastapi import Depends
from fastapi_users.authentication.strategy.db import DatabaseStrategy

from .dependencies.access_tokens_db import get_access_tokens_db
from core.config import settings

if TYPE_CHECKING:
    from core.models import AccessToken  # noqa
    from fastapi_users.authentication.strategy.db import AccessTokenDatabase  # noqa


def get_database_strategy(
    access_token_db: Annotated[
        "AccessTokenDatabase[AccessToken]",
        Depends(get_access_tokens_db),
    ],
) -> DatabaseStrategy:
    """
    Возвращает стратегию аутентификации, хранящую токены в базе данных.

    Эта стратегия используется для управления жизненным циклом токенов хранящихся в базе данных:
    - Создание
    - Проверка
    - Удаление (например, при выходе)
    - Контроль срока жизни

    Args:
        access_token_db (AccessTokenDatabase): Адаптер для работы с таблицей токенов.

    Returns:
        DatabaseStrategy: Экземпляр стратегии, использующей БД для хранения токенов.
    """
    return DatabaseStrategy(
        database=access_token_db,
        lifetime_seconds=settings.access_token.lifetime_seconds,
    )
