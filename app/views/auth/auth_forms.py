from fastapi import APIRouter, Request, Depends
from fastapi.responses import HTMLResponse
from fastapi_csrf_protect import CsrfProtect

from core.auth.dependencies.fastapi_users import optional_user
from core import templates

router = APIRouter()


@router.get(
    "/state",
    name="get_auth_state",
    include_in_schema=False,
    response_class=HTMLResponse,
)
async def get_auth_state(
    request: Request,
    user=Depends(optional_user),
    csrf_protect: CsrfProtect = Depends(),
):
    """Решает: показать форму входа или профиль при клике на иконку"""
    csrf_token, signed_token = csrf_protect.generate_csrf_tokens()

    if user:
        response = templates.TemplateResponse(
            request=request,
            name="auth/snippets/profile.html",
            context={
                "user": user,
                "csrf_token": csrf_token,
            },
        )
    else:
        response = templates.TemplateResponse(
            request=request,
            name="auth/snippets/login.html",
            context={"csrf_token": csrf_token},
        )

    csrf_protect.set_csrf_cookie(signed_token, response)
    return response


@router.get(
    "/register-form",
    name="get_register_form",
    include_in_schema=False,
    response_class=HTMLResponse,
)
async def get_register_form(
    request: Request,
    csrf_protect: CsrfProtect = Depends(),
):
    """Отдает форму регистрации для подмены в том же окне"""
    csrf_token, signed_token = csrf_protect.generate_csrf_tokens()

    response = templates.TemplateResponse(
        request=request,
        name="auth/snippets/register.html",
        context={"csrf_token": csrf_token},
    )
    csrf_protect.set_csrf_cookie(signed_token, response)
    return response


@router.get(
    "/terms-fragment",
    name="get_terms",
    include_in_schema=False,
    response_class=HTMLResponse,
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
    response_class=HTMLResponse,
)
async def get_login_form(
    request: Request,
    csrf_protect: CsrfProtect = Depends(),
):
    """Отдает форму входа (нужно для кнопки 'Назад' из регистрации)"""
    csrf_token, signed_token = csrf_protect.generate_csrf_tokens()
    response = templates.TemplateResponse(
        request=request,
        name="auth/snippets/login.html",
        context={
            "slide": True,
            "csrf_token": csrf_token,
        },
    )
    csrf_protect.set_csrf_cookie(signed_token, response)
    return response
