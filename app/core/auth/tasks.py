import logging

from datetime import datetime, timedelta, timezone
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from sqlalchemy import delete

from models.access_token import AccessToken
from models.user import User
from core import db_helper, settings

log = logging.getLogger(__name__)


scheduler = AsyncIOScheduler()


async def cleanup_expired_tokens():
    """Фоновая задача по очистке просроченных токенов из БД"""
    async with db_helper.session_factory() as session:
        try:
            now = datetime.now(timezone.utc)
            threshold = now - timedelta(seconds=settings.access_token.lifetime_seconds)
            statement = delete(AccessToken).where(AccessToken.created_at < threshold)
            result = await session.execute(statement)
            await session.commit()

            if result.rowcount > 0:
                log.info(f"Cleanup: Removed {result.rowcount} expired tokens from DB.")
        except Exception as e:
            log.error(f"Error during token cleanup: {e}")
            await session.rollback()


async def cleanup_unverified_users():
    """Удаляет неподтвержденных юзеров через 24 часа"""
    async with db_helper.session_factory() as session:
        try:
            now_utc = datetime.now(timezone.utc)
            threshold = now_utc - timedelta(hours=24)

            statement = delete(User).where(
                User.is_verified == False, User.created_at < threshold
            )
            result = await session.execute(statement)
            await session.commit()

            if result.rowcount > 0:
                log.info(f"Cleanup: Removed {result.rowcount} unverified users.")
        except Exception as e:
            log.error(f"User cleanup error: {e}")
            await session.rollback()


def setup_auth_scheduler():
    """Настройка расписания задач для модуля Auth"""
    scheduler.add_job(
        cleanup_expired_tokens,
        "interval",
        hours=12,
        id="token_cleanup",
        jitter=60,
    )
    scheduler.add_job(
        cleanup_unverified_users,
        "interval",
        hours=24,
        id="user_cleanup",
        jitter=120,
    )
    return scheduler
