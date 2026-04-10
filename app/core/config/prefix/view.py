from pydantic import BaseModel


class ViewPrefix(BaseModel):
    """Конфигурация префикса для страниц"""

    home: str = ""
    page_missing: str = "/page-missing"
    limit_exceeded: str = "/limit-exceeded"
    security_error: str = "/security-error"
    auth: str = "/auth"
