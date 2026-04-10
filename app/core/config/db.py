from pydantic import BaseModel, SecretStr
from sqlalchemy import URL


class SQLAlchemyConfig(BaseModel):
    """Конфигурация SQLAlchemy"""
    pool_size: int = 20
    max_overflow: int = 10
    echo: bool = False
    echo_pool: bool = False


class DataBaseConfig(BaseModel):
    """Конфигурация базы данных"""
    name: str
    host: str
    port: int
    user: str
    password: SecretStr

    sqla: SQLAlchemyConfig = SQLAlchemyConfig()

    naming_convention: dict[str, str] = {
        "ix": "ix_%(column_0_label)s",
        "uq": "uq_%(table_name)s_%(column_0_N_name)s",
        "ck": "ck_%(table_name)s_%(constraint_name)s",
        "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
        "pk": "pk_%(table_name)s",
    }

    @property
    def async_url(self) -> URL:
        return URL.create(
            drivername="postgresql+asyncpg",
            database=self.name,
            host=self.host,
            port=self.port,
            username=self.user,
            password=self.password.get_secret_value(),
        )