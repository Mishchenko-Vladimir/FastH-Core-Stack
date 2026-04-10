from fastapi import APIRouter

from core.auth.dependencies.fastapi_users import fastapi_users
from core.auth.backend import authentication_backend

from core import limiter
from core.config import settings
from schemas.user import UserRead, UserCreate

router = APIRouter(prefix=settings.api.v1.auth, tags=["Auth 🔐"])

# /login и /logout
login_router = fastapi_users.get_auth_router(authentication_backend)

# /register
register_router = fastapi_users.get_register_router(UserRead, UserCreate)

# /request-verify-token и /verify
verify_router = fastapi_users.get_verify_router(UserRead)

# /forgot-password и /reset-password
reset_router = fastapi_users.get_reset_password_router()

for route in login_router.routes:
    if route.path == "/login" and route.methods == {"POST"}:
        route.endpoint = limiter.limit("5/hour")(route.endpoint)

for route in register_router.routes:
    if route.path == "/register" and route.methods == {"POST"}:
        route.endpoint = limiter.limit("3/hour")(route.endpoint)

for route in reset_router.routes:
    if route.path == "/forgot-password" and route.methods == {"POST"}:
        route.endpoint = limiter.limit("2/hour")(route.endpoint)

router.include_router(login_router)
router.include_router(register_router)
router.include_router(verify_router)
router.include_router(reset_router)
