import asyncio
import logging

from fastapi_users import exceptions

from core import db_helper, settings
from core.auth.dependencies import user_manager_context, get_users_db_context
from core.auth.user_manager import UserManager
from models.user import User
from schemas.user import UserCreate

log = logging.getLogger(__name__)


async def create_user(
    user_manager: UserManager,
    user_create: UserCreate,
) -> User:
    user = await user_manager.create(
        user_create=user_create,
        safe=False,
    )
    return user


async def create_superuser() -> None:
    """
    Создаёт суперпользователя, если его ещё нет.
    Использует email и password из настроек.
    """
    async with db_helper.session_factory() as session:
        async with get_users_db_context(session) as users_db:
            async with user_manager_context(users_db, None) as user_manager:
                try:
                    user_exists = await user_manager.user_db.get_by_email(
                        settings.admin.admin_email
                    )
                    if user_exists:
                        if user_exists.is_superuser:
                            log.info(
                                "Суперпользователь %r уже существует.",
                                user_exists.email,
                            )
                        else:
                            log.warning(
                                "Пользователь %r существует, но не является суперпользователем.",
                                user_exists.email,
                            )
                        return None

                    user_create = UserCreate(
                        email=settings.admin.admin_email,
                        password=settings.admin.admin_password,
                        first_name="Admin",
                        is_active=True,
                        is_superuser=True,
                        is_verified=True,
                    )

                    try:
                        await create_user(
                            user_manager=user_manager,
                            user_create=user_create,
                        )
                        log.info("Создан суперпользователь: %r.", user_create.email)
                    except exceptions.UserAlreadyVerified:
                        log.info(
                            "Создан суперпользователь: %r.",
                            user_create.email,
                        )
                except Exception as exc:
                    log.error("Ошибка при создании суперпользователя: %r", exc)


if __name__ == "__main__":
    logging.basicConfig(
        level=settings.logging.log_level_value,
        format=settings.logging.log_format,
    )
    asyncio.run(create_superuser())
