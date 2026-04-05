from typing import Optional
from fastapi import APIRouter, Request, Form, Depends
from fastapi.responses import HTMLResponse
from fastapi_csrf_protect import CsrfProtect
from pydantic import EmailStr

from core.auth.dependencies.user_manager import get_user_manager
from core.auth.dependencies.fastapi_users import optional_user

from core import limiter, templates
from models.user import User

router = APIRouter()


@router.get(
    "/forgot-password",
    name="forgot_password",
    include_in_schema=False,
    response_class=HTMLResponse,
)
async def forgot_password(
    request: Request,
    csrf_protect: CsrfProtect = Depends(),
):
    """Отображение формы восстановления пароля"""
    csrf_token, signed_token = csrf_protect.generate_csrf_tokens()
    response = templates.TemplateResponse(
        request=request,
        name="auth/snippets/forgot-password.html",
        context={"csrf_token": csrf_token},
    )
    csrf_protect.set_csrf_cookie(signed_token, response)
    return response


@router.post(
    "/forgot-password",
    name="process_forgot_password",
    include_in_schema=False,
)
@limiter.limit("2/minute")
async def process_forgot_password(
    request: Request,
    email: Optional[EmailStr] = Form(None),
    user_manager=Depends(get_user_manager),
    current_user: Optional[User] = Depends(optional_user),
    csrf_protect: CsrfProtect = Depends(),
):
    """Обработка запроса на восстановление пароля"""
    await csrf_protect.validate_csrf(request)
    csrf_token, signed_token = csrf_protect.generate_csrf_tokens()

    if current_user:
        await user_manager.forgot_password(current_user, request)
        response = templates.TemplateResponse(
            request=request,
            name="auth/snippets/profile.html",
            context={
                "user": current_user,
                "success": "We’ve sent a password reset link to your email address.",
                "csrf_token": csrf_token,
            },
        )
    else:
        try:
            user = await user_manager.get_by_email(email)
            await user_manager.forgot_password(user, request)

        except Exception as e:
            pass

        response = templates.TemplateResponse(
            request=request,
            name="auth/snippets/forgot-password.html",
            context={
                "error": "If an account exists for that email, a reset link has been sent.",
                "csrf_token": csrf_token,
            },
        )
    csrf_protect.set_csrf_cookie(signed_token, response)
    return response


@router.get(
    "/password-reset",
    name="password_reset",
    include_in_schema=False,
    response_class=HTMLResponse,
)
def password_reset(
    request: Request,
    token: str,
    csrf_protect: CsrfProtect = Depends(),
):
    """Отображение страницы сброса пароля"""
    csrf_token, signed_token = csrf_protect.generate_csrf_tokens()

    response = templates.TemplateResponse(
        request=request,
        name="auth/reset-password.html",
        context={
            "token": token,
            "csrf_token": csrf_token,
        },
    )
    csrf_protect.set_csrf_cookie(signed_token, response)
    return response


@router.post(
    "/process_password_reset",
    name="process_password_reset",
    include_in_schema=False,
)
async def process_password_reset(
    request: Request,
    token: str = Form(...),
    password: str = Form(...),
    user_manager=Depends(get_user_manager),
    csrf_protect: CsrfProtect = Depends(),
):
    """Обработка сброса пароля"""
    await csrf_protect.validate_csrf(request)
    csrf_token, signed_token = csrf_protect.generate_csrf_tokens()

    try:
        await user_manager.reset_password(token, password, request)
        response = templates.TemplateResponse(
            request=request,
            name="auth/snippets/reset-password-inner.html",
            context={
                "success": True,
                "csrf_token": csrf_token,
            },
        )
    except Exception as e:
        response = templates.TemplateResponse(
            request=request,
            name="auth/snippets/reset-password-inner.html",
            context={
                "error": "Invalid token or weak password.",
                "token": token,
                "csrf_token": csrf_token,
            },
        )

    csrf_protect.set_csrf_cookie(signed_token, response)
    return response
