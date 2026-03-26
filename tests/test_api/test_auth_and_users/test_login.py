import pytest

from typing import Any
from httpx import AsyncClient


@pytest.mark.anyio
async def test_login_success(
    client: AsyncClient,
    registered_user: dict[str, Any],
    prefix_auth: str,
):
    """
    Успешный вход.
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


@pytest.mark.anyio
async def test_login_invalid_credentials(
    client: AsyncClient,
    registered_user: dict[str, Any],
    prefix_auth: str,
):
    """
    Вход с неверным паролем.
    """
    response = await client.post(
        url=f"{prefix_auth}/login",
        data={
            "username": registered_user["email"],
            "password": "wrong-password",
        },
        headers={"Content-Type": "application/x-www-form-urlencoded"},
    )
    assert response.status_code == 400
    assert response.json()["detail"] == "LOGIN_BAD_CREDENTIALS"


@pytest.mark.anyio
async def test_login_nonexistent_user(
    client: AsyncClient,
    prefix_auth: str,
):
    """
    Вход с несуществующим пользователем.
    """
    response = await client.post(
        url=f"{prefix_auth}/login",
        data={
            "username": "notexists@example.com",
            "password": "password123",
        },
        headers={"Content-Type": "application/x-www-form-urlencoded"},
    )
    assert response.status_code == 400
    assert response.json()["detail"] == "LOGIN_BAD_CREDENTIALS"
