from fastapi_csrf_protect import CsrfProtect
from core.config import settings


@CsrfProtect.load_config
def get_csrf_config():
    return settings.csrf.model_copy(
        update={"cookie_secure": settings.site.cookie_secure}
    )
