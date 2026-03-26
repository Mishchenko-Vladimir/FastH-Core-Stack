from fastapi import APIRouter, Depends
from fastapi.security import HTTPBearer

from .users import router as users_router
from .auth import router as auth_router

from core.config import settings


http_bearer = HTTPBearer(auto_error=False)

router = APIRouter(
    prefix=settings.api.v1.prefix,
    dependencies=[Depends(http_bearer)],
)

router.include_router(users_router)
router.include_router(auth_router)
