from fastapi_users.password import PasswordHelper
from sqladmin import ModelView
from starlette.requests import Request

from models.user import User

password_helper = PasswordHelper()


class UserAdmin(ModelView, model=User):
    """Админка для модели User"""

    name = "Пользователь"
    name_plural = "Пользователи"
    icon = "fa-solid fa-users"
    # Поля, которые будут отображаться в таблице
    column_list = [
        User.id,
        User.first_name,
        User.email,
        User.is_active,
        User.is_superuser,
        User.is_verified,
        User.created_at,
    ]
    # Форматирование отображения полей
    column_formatters = {
        # m — объект модели User
        # a — название атрибута ('created_at')
        User.created_at: lambda m, a: (
            m.created_at.strftime("%d.%m.%Y %H:%M") if m.created_at else ""
        )
    }
    # Переименование полей
    column_labels = {
        User.id: "ID",
        User.first_name: "Имя",
        User.email: "Email",
        User.is_active: "Активен",
        User.is_superuser: "Суперпользователь",
        User.is_verified: "Почта подтверждена",
        User.created_at: "Дата регистрации",
        User.hashed_password: "Password",
    }
    # Какие поля не показывать в форме редактирования
    form_excluded_columns = [
        User.access_tokens,
    ]
    # По каким столбцам будет осуществляться сортировка
    column_sortable_list = [
        User.id,
        User.is_superuser,
        User.is_verified,
        User.created_at,
    ]

    async def on_model_change(
        self,
        data: dict,
        model: User,
        is_created: bool,
        request: Request,
    ) -> None:
        """
        Метод вызывается при создании или изменении модели.
        Если при изменении модели пароль был пустой, то генерируем новый.

        :param data: Словарь с данными из формы (например, {"email": "user@example.com", "hashed_password": "123"})
        :param model: Текущий объект User из БД
        :param is_created: True, если создаём нового пользователя
        :param request: Объект запроса (можно получить текущего пользователя)
        :return:
        """
        # data may contain not hashed password
        raw_password = data.get("hashed_password") or password_helper.generate()
        if is_created or model.hashed_password != raw_password:
            data.update(
                hashed_password=password_helper.hash(raw_password),
            )
