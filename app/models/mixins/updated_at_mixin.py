from datetime import datetime, timezone
from sqlalchemy import func, DateTime
from sqlalchemy.orm import mapped_column, Mapped


class UpdatedAtMixin:
    """Миксин, добавляющий поле `updated_at` — для автоматического отслеживания времени изменения записи"""

    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
        server_default=func.now(),
        server_onupdate=func.now(),
        nullable=False,
        comment="Последнее обновление записи",
    )
