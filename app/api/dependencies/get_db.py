from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import AsyncSession

from core.db_helper import db_helper


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """
    Асинхронная зависимость для получения сессии SQLAlchemy.

    Предоставляет одну сессию из пула соединений через `db_helper.session_getter()`.
    Автоматически открывает и закрывает сессию при входе/выходе из контекста.
    Используется в FastAPI-роутерах через `Depends(get_db)`.
    """
    async for session in db_helper.session_getter():
        yield session
