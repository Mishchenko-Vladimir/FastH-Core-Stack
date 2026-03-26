from typing import Optional
from fastapi import APIRouter, Request, Form, Depends
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
)
async def forgot_password(request: Request):
    """Отображение формы восстановления пароля"""
    return templates.TemplateResponse(
        request=request,
        name="auth/snippets/forgot-password.html",
        context={},
    )


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
):
    """Обработка запроса на восстановление пароля"""
    if current_user:
        await user_manager.forgot_password(current_user, request)

        return templates.TemplateResponse(
            request=request,
            name="auth/snippets/profile.html",
            context={
                "user": current_user,
                "success": "We’ve sent a password reset link to your email address.",
            },
        )
    else:
        try:
            user = await user_manager.get_by_email(email)
            await user_manager.forgot_password(user, request)

        except Exception as e:
            pass

        return templates.TemplateResponse(
            request=request,
            name="auth/snippets/forgot-password.html",
            context={
                "error": "If an account exists for that email, a reset link has been sent."
            },
        )


@router.get(
    "/password-reset",
    name="password_reset",
    include_in_schema=False,
)
def password_reset(
    request: Request,
    token: str,
):
    """Отображение страницы сброса пароля"""
    return templates.TemplateResponse(
        request=request,
        name="auth/reset-password.html",
        context={"token": token},
    )


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
):
    """Обработка сброса пароля"""
    try:
        await user_manager.reset_password(token, password, request)
        return templates.TemplateResponse(
            request=request,
            name="auth/snippets/reset-password-inner.html",
            context={"success": True},
        )
    except Exception as e:
        return templates.TemplateResponse(
            request=request,
            name="auth/snippets/reset-password-inner.html",
            context={
                "error": "Invalid token or weak password.",
                "token": token,
            },
        )
