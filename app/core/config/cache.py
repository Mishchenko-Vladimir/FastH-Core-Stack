from pydantic import BaseModel


class RedisDB(BaseModel):
    """Настройки Redis"""

    cache: int = 0


class RedisConfig(BaseModel):
    """Настройки Redis"""

    host: str = "localhost"
    port: int = 6379
    db: RedisDB = RedisDB()


class CacheNamespace(BaseModel):
    """Именование пространства кэша"""

    users_list: str = "users-list"


class CacheConfig(BaseModel):
    """Настройки кэша"""

    enabled: bool = True
    prefix: str = "fastapi-cache"
    namespace: CacheNamespace = CacheNamespace()