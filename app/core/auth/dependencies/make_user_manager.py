import contextlib

from typing import Annotated, TYPE_CHECKING, Optional
from fastapi import Depends, BackgroundTasks

from core.auth.user_manager import UserManager
from .users_db import get_users_db

if TYPE_CHECKING:
    from fastapi_users_db_sqlalchemy import SQLAlchemyUserDatabase  # noqa


async def make_user_manager(
    user_db: Annotated["SQLAlchemyUserDatabase", Depends(get_users_db)],
    background_tasks: Optional[BackgroundTasks] = None,
):
    """
    Возвращает экземпляр UserManager для ручного использования
    (в CLI, админке, фоновых задачах).

    Используется, когда нельзя использовать зависимость get_user_manager.

    Args:
        user_db (SQLAlchemyUserDatabase): База данных пользователей
        background_tasks: BackgroundTasks или None

    Yields:
        UserManager: Менеджер пользователей
    """
    yield UserManager(
        user_db,
        background_tasks=background_tasks,
    )


user_manager_context = contextlib.asynccontextmanager(make_user_manager)
