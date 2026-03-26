import pytest

from typing import Any
from httpx import AsyncClient


@pytest.mark.anyio
async def test_get_current_user_profile(
    logged_in_client: AsyncClient,
    registered_user: dict[str, Any],
    prefix_users: str,
):
    """
    Тест: авторизованный пользователь может получить свой профиль через /me.
    """
    response = await logged_in_client.get(url=f"{prefix_users}/me")
    assert response.status_code == 200
    json = response.json()

    assert json["email"] == registered_user["email"]
    assert json["first_name"] == registered_user["first_name"]
    assert "id" in json
    assert json["is_active"] is True
    assert json["is_superuser"] is False


@pytest.mark.anyio
async def test_update_current_user_profile(
    logged_in_client: AsyncClient,
    prefix_users: str,
    fake_user_data: dict[str, Any],
):
    """
    Тест: авторизованный пользователь может обновить свои данные через /me.
    """
    new_first_name = fake_user_data["first_name"]

    response = await logged_in_client.patch(
        url=f"{prefix_users}/me",
        json={"first_name": new_first_name},
    )
    assert response.status_code == 200
    json = response.json()

    assert json["first_name"] == new_first_name


@pytest.mark.anyio
async def test_update_current_user_profile_invalid_email(
    logged_in_client: AsyncClient,
    prefix_users: str,
):
    """
    Тест: обновление email на уже существующий — ошибка.
    """

    response = await logged_in_client.patch(
        url=f"{prefix_users}/me",
        json={"email": "already.exists@example.com"},
    )

    if response.status_code == 400:
        assert "email" in response.json()["detail"].lower()


@pytest.mark.anyio
async def test_update_current_user_profile_unauthorized(
    client: AsyncClient,
    prefix_users: str,
):
    """
    Тест: неавторизованный пользователь не может обновить /me.
    """
    response = await client.patch(
        url=f"{prefix_users}/me",
        json={"first_name": "Hacker"},
    )
    assert response.status_code == 401


@pytest.mark.anyio
async def test_get_current_user_profile_unauthorized(
    client: AsyncClient,
    prefix_users: str,
):
    """
    Тест: неавторизованный пользователь не может получить /me.
    """
    response = await client.get(url=f"{prefix_users}/me")
    assert response.status_code == 401
