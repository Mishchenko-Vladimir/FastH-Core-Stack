from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import (
    create_async_engine,
    AsyncEngine,
    async_sessionmaker,
    AsyncSession,
)

from core.config import settings


class DatabaseHelper:
    """
    Утилита для управления асинхронным подключением к базе данных.

    Предоставляет:
    - Создание асинхронного движка (engine)
    - Фабрику сессий (session_factory)
    - Методы для получения и закрытия соединений

    Используется как Singleton (`db_helper`) для централизованного доступа к БД.

    Attributes:
        engine (AsyncEngine): Асинхронный движок SQLAlchemy
        session_factory (async_sessionmaker[AsyncSession]): Фабрика сессий

    Args:
        url (str): DSN-строка подключения к БД (например: postgresql+asyncpg://user:pass@host:port/dbname)
        echo (bool): Если True — выводит SQL-запросы в лог (по умолчанию False)
        echo_pool (bool): Если True — логирует действия пула соединений (не используется)
        pool_size (int): Размер пула соединений (не используется)
        max_overflow (int): Максимальное количество дополнительных соединений сверх пула
    """

    def __init__(
        self,
        url: str,
        echo: bool = False,
        echo_pool: bool = False,
        pool_size: int = 5,
        max_overflow: int = 10,
    ) -> None:
        self.engine: AsyncEngine = create_async_engine(
            url=url,
            echo=echo,
            # echo_pool=echo_pool,
            # pool_size=pool_size,
            max_overflow=max_overflow,
        )
        self.session_factory: async_sessionmaker[AsyncSession] = async_sessionmaker(
            bind=self.engine,
            autocommit=False,
            autoflush=False,
            expire_on_commit=False,
        )

    # Закрытие движка
    async def dispose(self) -> None:
        """
        Закрывает все соединения пула и освобождает ресурсы движка.
        Вызывается при завершении работы приложения.
        """
        await self.engine.dispose()

    # Для получения сессии
    async def session_getter(self) -> AsyncGenerator[AsyncSession, None]:
        """
        Генератор сессий для использования в FastAPI-зависимостях.
        Открывает сессию, предоставляет её и автоматически закрывает после использования.

        Yields:
            AsyncSession: Асинхронная сессия SQLAlchemy
        """
        async with self.session_factory() as session:
            yield session


# Глобальный экземпляр для использования в приложении
db_helper = DatabaseHelper(
    url=str(settings.db.url),
    echo=settings.db.echo,
    echo_pool=settings.db.echo_pool,
    pool_size=settings.db.pool_size,
    max_overflow=settings.db.max_overflow,
)
