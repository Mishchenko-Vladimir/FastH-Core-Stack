from fastapi import APIRouter, Request

from core import templates
from core.config import settings

router = APIRouter(prefix=settings.view.page_missing)


@router.get(
    "/",
    name="page_missing",
    include_in_schema=False,
    response_model=None,
)
def page_missing(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="page-missing.html",
        context={},
    )
