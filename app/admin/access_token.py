import secrets

from typing import Any
from sqladmin import ModelView
from starlette.requests import Request

from admin.converter import ModelConverter
from models.access_token import AccessToken


class AccessTokenAdmin(ModelView, model=AccessToken):
    """Админка токенов доступа"""

    name = "Токен доступа"
    name_plural = "Токены доступа"
    icon = "fa-solid fa-key"
    # Поля, которые будут отображаться в таблице
    column_list = [
        AccessToken.token,
        AccessToken.created_at,
        AccessToken.user,
    ]
    # Кастомный конвертер для полей created_at, что бы отображать как календарь с выбором времени, а не как строка
    form_converter = ModelConverter
    # Сортировка по умолчанию по полю дате создания
    column_default_sort = [
        (AccessToken.created_at, False),
    ]
    form_include_pk = True  # Показывать id в форме
    can_edit = False  # Запретить редактирование
    # Поля, которые не показывать в форме
    form_excluded_columns = [
        AccessToken.user_id,
        AccessToken.created_at,
    ]
    # Поля, которые можно заполнять при создании
    form_create_rules = [
        "user",
    ]

    def insert_model(
        self,
        request: Request,
        data: dict,
    ) -> Any:
        """При создании токена генерируем его автоматически"""
        if "token" not in data:
            data.update(token=secrets.token_urlsafe())
        return super().insert_model(
            request=request,
            data=data,
        )
