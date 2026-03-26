from fastapi_users import FastAPIUsers

from core.auth.backend import authentication_backend
from core.auth.user_id_type import UserIdType
from .user_manager import get_user_manager
from models.user import User


fastapi_users = FastAPIUsers[User, UserIdType](
    get_user_manager,
    [authentication_backend],
)

# Получение текущего пользователя, если он не зарегистрирован — None
optional_user = fastapi_users.current_user(optional=True)

# Получение активного пользователя
current_active_user = fastapi_users.current_user(active=True)

# Получение активного и подтверждённого пользователя
current_active_verified_user = fastapi_users.current_user(active=True, verified=True)

# Получение суперпользователя
current_active_superuser = fastapi_users.current_user(active=True, superuser=True)
