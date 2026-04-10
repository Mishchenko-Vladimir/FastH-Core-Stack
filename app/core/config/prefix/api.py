from pydantic import BaseModel


class ApiV1Prefix(BaseModel):
    """Конфигурация префикса API версии 1"""

    prefix: str = "/v1"
    webhooks: str = "/webhooks"
    auth: str = "/auth"
    users: str = "/users"


class ApiPrefix(BaseModel):
    """Конфигурация префикса API"""

    prefix: str = "/api"
    v1: ApiV1Prefix = ApiV1Prefix()

    @property
    def bearer_token_url(self) -> str:
        # api/v1/auth/login
        parts = (self.prefix, self.v1.prefix, self.v1.auth, "/login")
        path = "".join(parts)
        return path.removeprefix("/")  # Удаляем начальный /
