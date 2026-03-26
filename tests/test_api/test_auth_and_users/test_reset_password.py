import pytest

from typing import Any
from httpx import AsyncClient
from unittest.mock import AsyncMock, patch


@pytest.mark.anyio
async def test_forgot_password_success(
    client: AsyncClient,
    prefix_auth: str,
    registered_user: dict[str, Any],
):
    """
    Отправка письма на почту для сброса пароля.
    """
    with patch(
        target="services.mailing.send_reset_password.send_email",
        new_callable=AsyncMock,
    ) as mock:
        response = await client.post(
            url=f"{prefix_auth}/forgot-password",
            json={"email": registered_user["email"]},
        )
        assert response.status_code == 202
        assert mock.called


@pytest.mark.anyio
async def test_reset_password_invalid_token(
    client: AsyncClient,
    prefix_auth: str,
):
    """
    Сброс пароля с неверным токеном.
    """
    response = await client.post(
        url=f"{prefix_auth}/reset-password",
        json={"token": "invalid_token", "password": "newpass123"},
    )
    assert response.status_code == 400
