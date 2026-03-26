import pytest

from typing import Any
from httpx import AsyncClient
from faker import Faker

from core.config import settings


faker = Faker()


@pytest.fixture(scope="module")
def prefix_auth() -> str:
    """Префикс для всех auth-роутеров."""
    return f"{settings.api.prefix}{settings.api.v1.prefix}{settings.api.v1.auth}"


@pytest.fixture(scope="module")
def prefix_users() -> str:
    """Префикс для users-роутеров."""
    return f"{settings.api.prefix}{settings.api.v1.prefix}{settings.api.v1.users}"


@pytest.fixture(scope="function")
async def registered_user(
    client: AsyncClient,
    prefix_auth: str,
    fake_user_data: dict[str, Any],
) -> dict[str, Any]:
    """
    Регистрирует пользователя (через API) и возвращает его данные.
    """
    del fake_user_data["hashed_password"]
    fake_user_data["password"] = faker.password()

    response = await client.post(
        url=f"{prefix_auth}/register",
        json=fake_user_data,
    )
    assert response.status_code == 201
    return fake_user_data


@pytest.fixture(scope="function")
async def logged_in_client(
    client: AsyncClient,
    registered_user: dict[str, Any],
    prefix_auth: str,
) -> AsyncClient:
    """
    Возвращает клиент с активной сессией (кукой).
    """
    response = await client.post(
        url=f"{prefix_auth}/login",
        data={
            "username": registered_user["email"],
            "password": registered_user["password"],
        },
        headers={"Content-Type": "application/x-www-form-urlencoded"},
    )
    assert response.status_code == 204
    assert "fastapiusersauth" in response.cookies
    return client
