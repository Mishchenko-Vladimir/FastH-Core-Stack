from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse

from core import settings, templates

router = APIRouter(prefix=settings.view.security_error)


@router.get(
    "/",
    name="security_error",
    include_in_schema=False,
    response_class=HTMLResponse,
)
async def security_error(request: Request):
    """
    Отображает страницу ошибки безопасности (CSRF).
    Сюда пользователь попадает, если токен истек или подменен.
    """
    return templates.TemplateResponse(
        request=request,
        name="security-error.html",
        context={},
    )
