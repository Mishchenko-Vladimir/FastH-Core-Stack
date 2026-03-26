import logging

from typing import Union
from fastapi import Request
from sqladmin.authentication import AuthenticationBackend
from starlette.responses import RedirectResponse

from core import db_helper, settings
from core.auth.dependencies import (
    get_users_db_context,
    user_manager_context,
    get_access_token_db_context,
)
from core.auth.strategy import get_database_strategy


logger = logging.getLogger(__name__)


class AdminAuth(AuthenticationBackend):
    async def login(self, request: Request) -> bool:
        # Если публичный вход выключен — показываем форму в админке
        if not settings.admin.public_auth:
            form = await request.form()
            email = form.get("username")
            password = form.get("password")

            if not email or not password:
                return False

            background_tasks = getattr(request.state, "background", None)

            async with db_helper.session_factory() as session:
                async with get_users_db_context(session) as users_db:
                    async with user_manager_context(users_db, background_tasks) as user_manager:
                        user = await user_manager.user_db.get_by_email(email)
                        if not user or not user.is_superuser:
                            logger.warning("Суперпользователь не найден: %r", email)
                            return False

                        is_valid, _ = user_manager.password_helper.verify_and_update(password, user.hashed_password)
                        if not is_valid:
                            logger.warning("Неверный пароль для: %r", email)
                            return False

                        #  Получаем access_token_db
                        async with get_access_token_db_context(session) as access_token_db:
                            strategy = get_database_strategy(access_token_db)
                            token = await strategy.write_token(user)

                        request.session.update({"fastapiusersauth": token})
                        return True

        # Если публичный вход включён — редирект на сайт
        return False

    async def logout(self, request: Request) -> RedirectResponse:
        request.session.clear()
        return RedirectResponse(url="/")

    async def authenticate(self, request: Request) -> Union[bool, RedirectResponse]:
        try:
            # Если публичный вход выключен — проверяем сессию
            if not settings.admin.public_auth:
                cookie = request.session.get("fastapiusersauth")
                if not cookie:
                    return RedirectResponse(url="/admin/login")
            else:
                cookie = request.cookies.get("fastapiusersauth")
                if not cookie:
                    # Иначе — редирект на сайт
                    request.session.clear()
                    return RedirectResponse(url="/page-missing")

            background_tasks = getattr(request.state, "background", None)

            async with db_helper.session_factory() as session:
                async with get_users_db_context(session) as users_db:
                    async with user_manager_context(users_db, background_tasks) as user_manager:
                        async with get_access_token_db_context(session) as access_token_db:
                            strategy = get_database_strategy(access_token_db)
                            user = await strategy.read_token(cookie, user_manager)
                            if (
                                not user
                                or not user.is_active
                                or not user.is_verified
                                or not user.is_superuser
                            ):
                                request.session.clear()
                                return RedirectResponse(url="/page-missing")

                            request.session.update({"user_id": str(user.id)})
                            logger.info("User with id: %r, has logged into the admin-panel.", str(user.id))
                            return True

        except Exception as exc:
            logger.error("Authentication error in the admin-panel.", exc_info=True)
            request.session.clear()
            return RedirectResponse(url="/page-missing")
