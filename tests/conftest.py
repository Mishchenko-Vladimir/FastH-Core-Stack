import pytest

from contextlib import asynccontextmanager
from fastapi import FastAPI
from typing import AsyncIterator, Any
from httpx import AsyncClient, ASGITransport
from faker import Faker
from unittest.mock import patch, AsyncMock

from sqlalchemy.ext.asyncio import (
    AsyncSession,
    create_async_engine,
    async_sessionmaker,
)
from sqlalchemy.pool import StaticPool

from api import router as api_router
from api.dependencies.get_db import get_db
from create_fastapi_app import create_app
from core.db_helper import db_helper
from models import Base, User
from views import router as views_router

faker = Faker()

# Тестовая БД в памяти
TEST_DATABASE_URL = "sqlite+aiosqlite:///:memory:"


@pytest.fixture(scope="session")
def anyio_backend():
    """
    Фикстура, указывающая, какой асинхронный движок использовать (asyncio или trio)
    """
    return "asyncio"


@pytest.fixture(scope="session")
async def test_engine():
    """
    Создает тестовую БД и мигрирует модели в нее.
    """
    engine = create_async_engine(
        TEST_DATABASE_URL,
        echo=False,
        poolclass=StaticPool,
    )
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield engine
    await engine.dispose()


@pytest.fixture(scope="function")
async def test_session(test_engine):
    """
    Создает сессию для тестовой БД.
    :return: - откат изменений после каждого теста.
    """
    async_session = async_sessionmaker(
        bind=test_engine,
        expire_on_commit=False,
        autoflush=False,
        autocommit=False,
    )
    async with async_session() as session:
        yield session
        await session.rollback()


@asynccontextmanager
async def empty_lifespan(app: FastAPI) -> AsyncIterator[None]:
    """Пустой lifespan для тестов."""
    yield


@pytest.fixture(scope="function")
async def client(test_engine, test_session):
    """
    Создает тестовый клиент для тестирования API.
    """
    db_helper.engine = test_engine
    db_helper.session_factory = async_sessionmaker(
        bind=test_engine,
        expire_on_commit=False,
        autoflush=False,
        autocommit=False,
    )

    def override_get_session():
        """Заменяет реальную сессию на тестовую."""
        return test_session

    app: FastAPI = create_app(
        create_custom_static_urls=True,
        lifespan_override=empty_lifespan,
    )
    app.include_router(api_router)
    app.include_router(views_router)
    app.dependency_overrides[get_db] = override_get_session  # type: ignore

    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://test",
    ) as ac:
        yield ac

    app.dependency_overrides.clear()  # type: ignore


@pytest.fixture(autouse=True)
def mock_aiosmtplib():
    """
    Автоматически подменяет отправку почты на пустышку для всех тестов.
    Теперь aiosmtplib.send не будет пытаться соединиться с 127.0.0.1.
    """
    with patch("aiosmtplib.send", new_callable=AsyncMock) as mock:
        yield mock


@pytest.fixture(scope="function")
def fake_user_data() -> dict[str, Any]:
    """
    Генерация тестовых данных пользователя.
    """
    return {
        "email": faker.email(),
        "hashed_password": faker.password(),
        "first_name": faker.first_name(),
        "is_active": True,
        "is_superuser": False,
    }


@pytest.fixture(scope="function")
async def test_user(
    test_session: AsyncSession,
    fake_user_data: dict[str, Any],
) -> User:
    """
    Создаёт тестового пользователя.
    """
    user = User(**fake_user_data)
    test_session.add(user)
    await test_session.commit()
    await test_session.refresh(user)
    return user
