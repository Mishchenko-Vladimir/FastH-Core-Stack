from typing import TYPE_CHECKING
from fastapi_users_db_sqlalchemy.access_token import (
    SQLAlchemyAccessTokenDatabase,
    SQLAlchemyBaseAccessTokenTable,
)
from sqlalchemy import ForeignKey, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base
from core.auth.user_id_type import UserIdType

if TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncSession  # noqa
    from .user import User  # noqa


class AccessToken(Base, SQLAlchemyBaseAccessTokenTable[UserIdType]):
    """Таблица для хранения access_token."""

    user_id: Mapped[UserIdType] = mapped_column(
        Integer,
        ForeignKey("users.id", ondelete="cascade"),
        nullable=False,
    )

    user: Mapped["User"] = relationship(back_populates="access_tokens")

    @classmethod
    def get_db(cls, session: "AsyncSession"):
        return SQLAlchemyAccessTokenDatabase(session, cls)

    def __str__(self):
        return self.token
