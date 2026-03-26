from fastapi import APIRouter, Request, Depends
from fastapi_users import exceptions

from core.auth.dependencies.user_manager import get_user_manager
from core.auth.dependencies.fastapi_users import current_active_user

from core.templates import templates
from models.user import User

router = APIRouter()


@router.post(
    "/request-verify-email",
    name="request_verify_email",
    include_in_schema=False,
)
async def request_verify_email(
    request: Request,
    user: User = Depends(current_active_user),
    user_manager=Depends(get_user_manager),
):
    """Отправка письма для верификации email в профиле"""
    try:
        await user_manager.request_verify(user, request)

        return templates.TemplateResponse(
            request=request,
            name="auth/snippets/profile.html",
            context={
                "user": user,
                "verify_messages": "Verification link sent to your email",
            },
        )

    except Exception as e:
        return templates.TemplateResponse(
            request=request,
            name="auth/snippets/profile.html",
            context={
                "user": user,
                "error_messages": "Could not send email. Try again later.",
            },
        )


@router.get(
    "/verify-email",
    name="verify_email",
    include_in_schema=False,
)
async def verify_email(
    request: Request,
    token: str,
    user_manager=Depends(get_user_manager),
):
    """Верификация email"""
    try:
        user = await user_manager.verify(token, request)

        return templates.TemplateResponse(
            request=request,
            name="auth/verify-result.html",
            context={
                "user": user,
                "success": True,
                "message": "Your email has been successfully verified!",
            },
        )
    except (
        exceptions.InvalidVerifyToken,
        exceptions.UserAlreadyVerified,
        exceptions.UserNotExists,
    ):
        return templates.TemplateResponse(
            request=request,
            name="auth/verify-result.html",
            context={
                "success": False,
                "message": "The verification link is invalid or has expired.",
            },
        )
