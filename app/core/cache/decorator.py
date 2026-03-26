from fastapi_cache import FastAPICache
from fastapi_cache.decorator import cache

from core.config import settings


def conditional_cache(*cache_args, **cache_kwargs):
    """
    Условный декоратор кэширования: применяет кэширование только если оно включено в настройках
    и окружение не является тестовым.

    Args:
        *cache_args: Позиционные аргументы для @cache (например, время жизни).
        **cache_kwargs: Именованные аргументы для @cache.

    Returns:
        Callable: Декоратор @cache или обёртка без кэширования.
    """
    if not settings.cache.enabled or settings.site.environment == "testing":
        return lambda func: func

    # Иначе — применяем настоящий @cache
    return cache(*cache_args, **cache_kwargs)


async def noop(*args, **kwargs) -> None:
    """Пустая асинхронная функция для безопасного `await`."""
    pass


def conditional_clear(*args, **kwargs):
    """
    Условная очистка кэша: вызывает `FastAPICache.clear()` только если кэширование включено и не является тестовым.

    Предотвращает попытки очистки кэша, когда он отключён (например, в тестах или dev-среде).
    Безопасно использовать в любом окружении.

    Args:
        *args: Позиционные аргументы для `FastAPICache.clear()` (например, `namespace`).
        **kwargs: Именованные аргументы для `FastAPICache.clear()` (например, `prefix`).

    Returns:
        Awaitable[None] | None: Результат `FastAPICache.clear()` (если кэш включён), иначе `None`.
    """
    if settings.cache.enabled and settings.site.environment != "testing":
        return FastAPICache.clear(*args, **kwargs)
    return noop()
