from fastapi import APIRouter

from .home import router as home_router
from .page_missing import router as page_missing_router
from .limit_exceeded import router as limit_exceeded_router
from .security_error import router as security_error_router

from views.auth import router as auth_router

router = APIRouter()

router.include_router(home_router)
router.include_router(page_missing_router)
router.include_router(limit_exceeded_router)
router.include_router(auth_router)
router.include_router(security_error_router)
