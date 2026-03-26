import pytest

from httpx import AsyncClient


@pytest.mark.anyio
async def test_logout_success(
    logged_in_client: AsyncClient,
    prefix_auth: str,
):
    """
    Успешный выход.
    """
    response = await logged_in_client.post(url=f"{prefix_auth}/logout")

    assert response.status_code == 204
    assert "fastapiusersauth" not in response.cookies
