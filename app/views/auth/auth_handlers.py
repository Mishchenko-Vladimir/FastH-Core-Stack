import logging

from fastapi import APIRouter, Request, Depends, Form
from fastapi.security import OAuth2PasswordRequestForm
from fastapi_users import exceptions
from pydantic import EmailStr, ValidationError

from core.auth.dependencies import (
    get_user_manager,
    get_access_tokens_db,
)
from core.auth.strategy import get_database_strategy
from core.auth.transport import cookie_transport

from core import limiter, templates
from schemas.user import UserCreate

log = logging.getLogger(__name__)

router = APIRouter()


@router.post(
    "/login-handler",
    name="login_handler",
    include_in_schema=False,
)
@limiter.limit("6/minute")
async def login_handler(
    request: Request,
    username: str = Form(...),
    password: str = Form(...),
    user_manager=Depends(get_user_manager),
    access_token_db=Depends(get_access_tokens_db),
):
    """Обрабатывает запрос входа"""
    try:
        credentials = OAuth2PasswordRequestForm(
            username=username,
            password=password,
        )
        user = await user_manager.authenticate(credentials)

        if not user:
            return templates.TemplateResponse(
                request=request,
                name="auth/snippets/login.html",
                context={"error": "Invalid email or password"},
            )
        if not user.is_verified:
            try:
                await user_manager.request_verify(user, request)
                msg = "Email not verified. We've sent a new link to your inbox."
            except Exception:
                msg = "Email not verified. Please check your inbox or try again later."

            return templates.TemplateResponse(
                request=request,
                name="auth/snippets/login.html",
                context={"success": msg},
            )

        strategy = get_database_strategy(access_token_db)
        token = await strategy.write_token(user)

        response = templates.TemplateResponse(
            request=request,
            name="auth/snippets/profile.html",
            context={"user": user},
        )

        response.set_cookie(
            key=cookie_transport.cookie_name,
            value=token,
            max_age=cookie_transport.cookie_max_age,
            path=cookie_transport.cookie_path,
            domain=cookie_transport.cookie_domain,
            secure=cookie_transport.cookie_secure,
            httponly=cookie_transport.cookie_httponly,
            samesite=cookie_transport.cookie_samesite,
        )
        response.headers["HX-Trigger"] = "userLoggedIn"
        response.headers["HX-Refresh"] = "true"
        return response

    except Exception as e:
        log.warning("An internal server error has occurred: %r.", e)
        return templates.TemplateResponse(
            request=request,
            name="auth/snippets/login.html",
            context={"error": "Internal Server Error."},
        )


@router.post(
    "/logout-handler",
    name="logout_handler",
    include_in_schema=False,
)
async def logout_handler(
    request: Request,
    access_token_db=Depends(get_access_tokens_db),
):
    """Обрабатывает запрос выхода и удаляет токен"""

    token = request.cookies.get("fastapiusersauth")

    if token:
        strategy = get_database_strategy(access_token_db)
        await strategy.destroy_token(token, None)  # type: ignore

    response = templates.TemplateResponse(
        request=request,
        name="auth/snippets/login.html",
        context={},
    )

    response.delete_cookie(key="fastapiusersauth", path="/")
    response.headers["HX-Trigger"] = "userLoggedOut"
    response.headers["HX-Refresh"] = "true"
    return response


@router.post(
    "/register-handler",
    name="register_handler",
    include_in_schema=False,
)
@limiter.limit("3/minute")
async def register_handler(
    request: Request,
    email: EmailStr = Form(...),
    password: str = Form(...),
    first_name: str = Form(...),
    agreed: bool = Form(False),
    user_manager=Depends(get_user_manager),
):
    """Обрабатывает запрос регистрации"""
    if not agreed:
        return templates.TemplateResponse(
            request=request,
            name="auth/snippets/register.html",
            context={"error": "You must agree to the terms"},
        )
    try:
        await user_manager.create(
            UserCreate(email=email, password=password, first_name=first_name),
            safe=True,
            request=request,
        )

        return templates.TemplateResponse(
            request=request,
            name="auth/snippets/login.html",
            context={
                "success": "Registration successful! Please check your email to verify your account before logging in.",
                "slide": True,
            },
        )

    except ValidationError as e:
        error_msg = e.errors()[0]["msg"]
        return templates.TemplateResponse(
            request=request,
            name="auth/snippets/register.html",
            context={"error": f"Validation error: {error_msg}"},
        )
    except exceptions.UserAlreadyExists:
        return templates.TemplateResponse(
            request=request,
            name="auth/snippets/register.html",
            context={"error": "User with this email already exists"},
        )
    except Exception as e:
        log.warning("Register Error: %r.", e)
        return templates.TemplateResponse(
            request=request,
            name="auth/snippets/register.html",
            context={"error": "Registration failed. Try again."},
        )
