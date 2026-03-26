from fastapi import APIRouter

from core import settings

from .auth_forms import router as auth_forms_router
from .auth_handlers import router as auth_handlers_router
from .password_changes import router as password_changes_router
from .verify_email import router as verify_email_router

router = APIRouter(prefix=settings.view.auth)

router.include_router(auth_forms_router)
router.include_router(auth_handlers_router)
router.include_router(password_changes_router)
router.include_router(verify_email_router)
