from sqlalchemy import MetaData
from sqlalchemy.orm import DeclarativeBase, declared_attr

from core.config import settings
from utils.case_converter import camel_case_to_snake_case


class Base(DeclarativeBase):
    """Базовая модель для всех таблиц"""

    __abstract__ = True

    # Для имен миграций
    metadata = MetaData(naming_convention=settings.db.naming_convention)

    @declared_attr.directive
    def __tablename__(cls) -> str:
        """Конвертация имени таблицы"""
        return f"{camel_case_to_snake_case(cls.__name__)}s"
