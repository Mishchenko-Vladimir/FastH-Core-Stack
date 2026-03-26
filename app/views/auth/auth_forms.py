from fastapi import APIRouter, Request, Depends

from core.auth.dependencies.fastapi_users import optional_user
from core import settings, templates

router = APIRouter()


@router.get(
    "/state",
    name="get_auth_state",
    include_in_schema=False,
)
async def get_auth_state(
    request: Request,
    user=Depends(optional_user),
):
    """Решает: показать форму входа или профиль при клике на иконку"""
    if user:
        return templates.TemplateResponse(
            request=request,
            name="auth/snippets/profile.html",
            context={"user": user},
        )
    return templates.TemplateResponse(
        request=request,
        name="auth/snippets/login.html",
        context={},
    )


@router.get(
    "/register-form",
    name="get_register_form",
    include_in_schema=False,
)
async def get_register_form(request: Request):
    """Отдает форму регистрации для подмены в том же окне"""
    return templates.TemplateResponse(
        request=request,
        name="auth/snippets/register.html",
        context={},
    )


@router.get(
    "/terms-fragment",
    name="get_terms",
    include_in_schema=False,
)
async def get_terms(request: Request):
    """Отдает форму правил и условий в том же окне"""
    return templates.TemplateResponse(
        request=request,
        name="auth/snippets/terms.html",
        context={},
    )


@router.get(
    "/login-form",
    name="login_form",
    include_in_schema=False,
)
async def get_login_form(request: Request):
    """Отдает форму входа (нужно для кнопки 'Назад' из регистрации)"""
    return templates.TemplateResponse(
        request=request,
        name="auth/snippets/login.html",
        context={"slide": True},
    )
