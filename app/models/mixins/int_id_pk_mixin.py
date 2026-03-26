from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column


class IntIdPkMixin:
    """Миксин, добавляющий автоинкрементное целочисленное поле `id` как первичный ключ."""

    id: Mapped[int] = mapped_column(primary_key=True)
