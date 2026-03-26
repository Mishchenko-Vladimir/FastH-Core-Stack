from fastapi import APIRouter, Request

from core import settings, limiter, templates


router = APIRouter(prefix=settings.view.limit_exceeded)


@router.get(
    "/",
    name="limit_exceeded",
    include_in_schema=False,
    response_model=None,
)
@limiter.exempt
def limit_exceeded(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="limit-exceeded.html",
        context={},
    )
