from typing import TYPE_CHECKING
from fastapi_users_db_sqlalchemy import (
    SQLAlchemyBaseUserTable,
    SQLAlchemyUserDatabase as SQLAlchemyUserDatabaseGeneric,
)
from sqlalchemy import String, select
from sqlalchemy.orm import Mapped, mapped_column, relationship

from core.auth.user_id_type import UserIdType
from .base import Base
from .mixins import IntIdPkMixin, CreatedAtMixin

if TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncSession  # noqa
    from .access_token import AccessToken  # noqa


class SQLAlchemyUserDatabase(SQLAlchemyUserDatabaseGeneric):
    """
    Добавление новых методов в SQLAlchemyUserDatabase, для работы с пользователями.

    Methods:
        get_users() Возвращает список пользователей.
    """

    async def get_users(self) -> list["User"]:
        """Возвращает список пользователей."""
        statement = select(User).order_by(User.id)
        results = await self.session.scalars(statement)
        return list(results.all())


class User(
    Base,
    IntIdPkMixin,
    CreatedAtMixin,
    SQLAlchemyBaseUserTable[UserIdType],
):
    """Таблица пользователей"""

    first_name: Mapped[str] = mapped_column(
        String(64),
        comment="Имя пользователя",
    )

    access_tokens: Mapped[list["AccessToken"]] = relationship(back_populates="user")

    @classmethod
    def get_db(cls, session: "AsyncSession"):
        """Получение данных из БД"""
        return SQLAlchemyUserDatabase(session, cls)

    def __str__(self):
        return self.email
