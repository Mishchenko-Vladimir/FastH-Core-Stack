from datetime import datetime, UTC, timezone
from sqlalchemy import func, DateTime
from sqlalchemy.orm import mapped_column, Mapped


class CreatedAtMixin:
    """Миксин, добавляющий поле `created_at` с поддержкой часового пояса"""

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        server_default=func.now(),
        index=True,
        nullable=False,
        comment="Дата создания записи",
    )
