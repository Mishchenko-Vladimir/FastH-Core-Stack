import contextlib

from typing import TYPE_CHECKING, Annotated
from fastapi import Depends

from core.db_helper import db_helper
from models.user import User

if TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncSession  # noqa


async def get_users_db(
    session: Annotated["AsyncSession", Depends(db_helper.session_getter)],
):
    """
    Зависимость для получения базы данных пользователей.

    Возвращает адаптер для работы с моделью User через SQLAlchemy.
    Используется UserManager для выполнения CRUD операций.

    Args:
        session (AsyncSession): Асинхронная сессия

    Yields:
        SQLAlchemyUserDatabase: Адаптер для User
    """
    yield User.get_db(session=session)


get_users_db_context = contextlib.asynccontextmanager(get_users_db)
