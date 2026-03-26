from typing import Annotated, TYPE_CHECKING
from fastapi import Depends, BackgroundTasks

from core.auth.user_manager import UserManager
from .users_db import get_users_db

if TYPE_CHECKING:
    from fastapi_users_db_sqlalchemy import SQLAlchemyUserDatabase  # noqa


async def get_user_manager(
    user_db: Annotated["SQLAlchemyUserDatabase", Depends(get_users_db)],
    background_tasks: BackgroundTasks,
):
    """
    Зависимость для получения UserManager.

    Создаёт экземпляр UserManager с подключённой базой данных пользователей
    и фоновыми задачами. Используется FastAPI Users для управления
    регистрацией, входом, подтверждением почты и сбросом пароля.

    Args:
        user_db (SQLAlchemyUserDatabase): База данных пользователей
        background_tasks (BackgroundTasks): Фоновые задачи (email)

    Yields:
        UserManager: Менеджер пользователей
    """
    yield UserManager(
        user_db,
        background_tasks=background_tasks,
    )
