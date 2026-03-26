from fastapi import APIRouter

from core.config import settings


webhooks_router = APIRouter(prefix=settings.api.v1.webhooks)
