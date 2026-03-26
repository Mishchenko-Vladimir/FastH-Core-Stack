import pytest

from httpx import AsyncClient


@pytest.mark.anyio
async def test_request_verify_token_nonexistent_user(
    client: AsyncClient,
    prefix_auth: str,
):
    """
    Запрос токена для несуществующего пользователя — должен вернуть 202.
    """
    response = await client.post(
        url=f"{prefix_auth}/request-verify-token",
        json={"email": "notexists@example.com"},
    )
    assert response.status_code == 202


@pytest.mark.anyio
async def test_request_verify_token_invalid_email(
    client: AsyncClient,
    prefix_auth: str,
):
    """
    Запрос токена с невалидным email — 422.
    """
    response = await client.post(
        url=f"{prefix_auth}/request-verify-token",
        json={"email": "invalid-email"},
    )
    assert response.status_code == 422


@pytest.mark.anyio
async def test_verify_email_invalid_token(
    client: AsyncClient,
    prefix_auth: str,
):
    """
    Верификация с неверным токеном — 400.
    """
    response = await client.post(
        url=f"{prefix_auth}/verify",
        json={"token": "invalid_token"},
    )
    assert response.status_code == 400
    assert response.json()["detail"] == "VERIFY_USER_BAD_TOKEN"


@pytest.mark.anyio
async def test_verify_email_empty_token(
    client: AsyncClient,
    prefix_auth: str,
):
    """
    Верификация с пустым токеном — 400.
    """
    response = await client.post(
        url=f"{prefix_auth}/verify",
        json={"token": ""},
    )
    assert response.status_code == 400
    assert response.json()["detail"] == "VERIFY_USER_BAD_TOKEN"


@pytest.mark.anyio
async def test_verify_email_missing_token(
    client: AsyncClient,
    prefix_auth: str,
):
    """
    Верификация без токена — 422.
    """
    response = await client.post(
        url=f"{prefix_auth}/verify",
        json={},
    )
    assert response.status_code == 422
