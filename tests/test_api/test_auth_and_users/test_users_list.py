import pytest

from httpx import AsyncClient


@pytest.mark.anyio
async def test_get_users_list_unauthorized(
    client: AsyncClient,
    prefix_users: str,
):
    """
    Неавторизованный пользователь может получить список.
    """
    response = await client.get(url=prefix_users)
    assert response.status_code == 200
    assert isinstance(response.json(), list)


@pytest.mark.anyio
async def test_get_users_list_authorized(
    logged_in_client: AsyncClient,
    prefix_users: str,
):
    """
    Авторизованный пользователь может получить список.
    """
    response = await logged_in_client.get(url=prefix_users)
    assert response.status_code == 200
    assert isinstance(response.json(), list)
