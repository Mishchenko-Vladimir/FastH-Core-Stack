from fastapi_users import schemas
from pydantic import Field

from core.auth.user_id_type import UserIdType


class UserCreate(schemas.BaseUserCreate):
    """Схема создания пользователя"""

    first_name: str = Field(
        min_length=1,
        max_length=64,
        description="Имя пользователя",
    )


class UserUpdate(schemas.BaseUserUpdate):
    """Схема обновления пользователя"""

    first_name: str = Field(
        min_length=1,
        max_length=50,
        description="Имя пользователя",
    )


class UserRead(schemas.BaseUser[UserIdType]):
    """Схема для чтения пользователя"""

    first_name: str = Field(
        min_length=1,
        max_length=64,
        description="Имя пользователя",
    )
