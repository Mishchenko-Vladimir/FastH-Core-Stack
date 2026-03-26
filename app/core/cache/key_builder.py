import hashlib
from typing import (
    Any,
    Callable,
    Dict,
    Optional,
    Tuple,
)
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Request, Response

from models.user import SQLAlchemyUserDatabase


def universal_list_key_builder(
    func: Callable[..., Any],
    namespace: str,
    *,
    request: Optional[Request] = None,
    response: Optional[Any] = None,
    args: Tuple[Any, ...],
    kwargs: Dict[str, Any],
) -> str:
    """
    Формирует уникальный ключ кэша, игнорирует session.
    """

    exclude_types = (AsyncSession,)
    cache_kw = {k: v for k, v in kwargs.items() if not isinstance(v, exclude_types)}

    path = request.scope.get("path", "") if request else ""
    method = request.scope.get("method", "GET") if request else ""

    key_str = f"{func.__module__}:{func.__name__}:{method}:{path}:{cache_kw}"
    cache_key = hashlib.md5(key_str.encode()).hexdigest()

    return f"{namespace}:{cache_key}"


def users_list_key_builder(
    func: Callable[..., Any],
    namespace: str,
    *,
    request: Optional[Request] = None,
    response: Optional[Response] = None,
    args: Tuple[Any, ...],
    kwargs: Dict[str, Any],
) -> str:
    """
    Функция для построения ключа кэша для списка пользователей.
    """
    exclude_types = (SQLAlchemyUserDatabase,)
    cache_kw = {}
    for name, value in kwargs.items():
        if isinstance(value, exclude_types):
            continue
        cache_kw[name] = value

    path = request.scope.get("path", "") if request else ""
    method = request.scope.get("method", "GET") if request else ""

    key_str = f"{func.__module__}:{func.__name__}:{method}:{path}:{cache_kw}"
    cache_key = hashlib.md5(key_str.encode()).hexdigest()
    return f"{namespace}:{cache_key}"


def user_key_builder(
    func: Callable[..., Any],
    namespace: str,
    *,
    request: Optional[Request] = None,
    response: Optional[Any] = None,
    args: Tuple[Any, ...],
    kwargs: Dict[str, Any],
) -> str:
    """
    Формирует уникальный ключ кэша для пользователя по его ID или токену.
    Игнорирует AsyncSession.
    """

    exclude_types = (
        AsyncSession,
        SQLAlchemyUserDatabase,
    )
    filtered_kwargs = {
        k: v for k, v in kwargs.items() if not isinstance(v, exclude_types)
    }

    user = filtered_kwargs.get("user")
    user_id = getattr(user, "id", None)

    if user_id is not None:
        key_suffix = f"user:{user_id}"
    else:
        key_suffix = "anonymous"

    key_str = f"{func.__module__}:{func.__name__}:{key_suffix}"
    cache_key = hashlib.md5(key_str.encode()).hexdigest()

    return f"{namespace}:{cache_key}"


def get_by_name_key_builder(
    func: Callable[..., Any],
    namespace: str,
    *,
    request: Optional[Request] = None,
    response: Optional[Any] = None,
    args: Tuple[Any, ...],
    kwargs: Dict[str, Any],
) -> str:
    """
    Формирует уникальный ключ кэша для метода get_by_name.
    Учитывает имя товара и тип ресурса, игнорируя AsyncSession.
    """

    exclude_types = (AsyncSession,)
    filtered_kwargs = {
        k: v for k, v in kwargs.items() if not isinstance(v, exclude_types)
    }

    name_param = next((v for k, v in filtered_kwargs.items() if "name" in k), None)

    if name_param is None:
        raise ValueError("Не найден параметр 'name' в запросе")

    path = request.scope.get("path", "") if request else ""
    method = request.scope.get("method", "GET") if request else ""

    key_str = f"{func.__module__}:{func.__name__}:{method}:{path}:{name_param}"
    cache_key = hashlib.md5(key_str.encode()).hexdigest()

    return f"{namespace}:{cache_key}"


def get_by_id_key_builder(
    func: Callable[..., Any],
    namespace: str,
    *,
    request: Optional[Request] = None,
    response: Optional[Any] = None,
    args: Tuple[Any, ...],
    kwargs: Dict[str, Any],
) -> str:
    """
    Формирует уникальный ключ кэша для метода get_by_id.
    Учитывает id товара и тип ресурса.
    """

    exclude_types = (AsyncSession,)
    filtered_kwargs = {
        k: v for k, v in kwargs.items() if not isinstance(v, exclude_types)
    }

    id_param = next((v for k, v in filtered_kwargs.items() if "id" in k), None)

    if id_param is None:
        raise ValueError("Не найден параметр 'id' в запросе")

    path = request.scope.get("path", "") if request else ""
    method = request.scope.get("method", "GET") if request else ""

    key_str = f"{func.__module__}:{func.__name__}:{method}:{path}:{id_param}"
    cache_key = hashlib.md5(key_str.encode()).hexdigest()

    return f"{namespace}:{cache_key}"
