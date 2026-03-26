from fastapi import APIRouter, Request

from core import settings, templates


router = APIRouter(prefix=settings.view.home)


@router.get(
    "/",
    name="home",
    include_in_schema=False,
    response_model=None,
)
def home(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={},
    )
