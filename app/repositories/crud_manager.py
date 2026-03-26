from sqlalchemy import select
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession

from typing import (
    Type,
    TypeVar,
    Sequence,
    Generic,
    Any,
)

from models.base import Base


T = TypeVar("T", bound=Base)


class CrudManager(Generic[T]):
    """
    Универсальный CRUD-менеджер для работы с любой моделью SQLAlchemy.

    Предоставляет базовые операции: создание, чтение, обновление, удаление.
    Поддерживает работу с любыми моделями, унаследованными от `Base`.

    Attributes:
        session (AsyncSession): Асинхронная сессия SQLAlchemy для работы с БД
        model_db (Type[T]): Модель, с которой будет работать менеджер

    Args:
        session (AsyncSession): Асинхронная сессия SQLAlchemy
        model_db: Модель БД (например: User, Order, Product, Boat и т.д.)

    Methods:
        create(data): - Создаёт новую запись в БД.
        get_by_id(instance_id): - Получает запись по id.
        get_by_id_with_relations(instance_id, *relations): - Получает запись по id с подгруженными связями.
        get_all_by_field(field, value): - Получает все записи по полю.
        get_all_by_fields(**filters): - Получает все записи по нескольким полям.
        get_all(): - Получает все записи модели.
        update(instance, data): - Обновляет существующую запись.
        delete(instance): - Удаляет запись из БД.
    """

    def __init__(
        self,
        session: AsyncSession,
        model_db: Type[T],
    ):
        self.session = session
        self.model_db = model_db

    async def create(self, data) -> T:
        """
        Создаёт новую запись в базе данных.

        Args:
            data: Pydantic-схема с данными для создания

        Returns:
            T: Созданный экземпляр модели с заполненным `id` и `created_at`
        """
        instance = self.model_db(**data.model_dump())
        self.session.add(instance)
        await self.session.commit()
        await self.session.refresh(instance)
        return instance

    async def get_by_id(self, instance_id: int) -> T | None:
        """
        Получает одну запись по её уникальному идентификатору.

        Args:
            instance_id (int): Уникальный идентификатор записи

        Returns:
            T | None: Экземпляр модели или None, если не найден
        """
        stmt = select(self.model_db).where(self.model_db.id == instance_id)  # type: ignore
        result = await self.session.execute(stmt)
        return result.scalars().first()

    async def get_all_by_field_with_relations(
        self,
        field: str,
        value: Any,
        *relations: tuple[str, Type[Base]],
    ) -> Sequence[T]:
        """
        Получает объекты по полю field со значением value с подгруженными связями.

        Пример:
            favorite = await manager(session, Favorite).get_by_id_with_relations(
                - "id",
                - 123,
                - ("product", Product),
                - ("images", ImagePath),
            )

            SQLAlchemy-запрос будет выглядеть так:
                select(Favorite).options(
                    selectinload(Favorite.product)
                    .selectinload(Product.images)
                )
                .where(Favorite.id == 123)

        Args:
            field: Название поля модели
            value: Значение поля
            *relations: Цепочка связей в формате (attr_name, Model). Может быть одна или более

        Returns:
            Sequence[T]: Объекты с подгруженными связями или None

        Raises:
            ValueError: Если указанное поле field отсутствует в модели
            AttributeError: Если указанное поле не существует в модели
        """
        if not hasattr(self.model_db, field):
            raise ValueError(f"Модель {self.model_db.__name__} не имеет поля '{field}'")

        stmt = select(self.model_db).where(getattr(self.model_db, field) == value)  # type: ignore

        if not relations:
            result = await self.session.execute(stmt)
            return result.scalars().first()

        current_load = None
        prev_model = self.model_db

        for attr_name, next_model in relations:
            if not hasattr(prev_model, attr_name):
                raise AttributeError(
                    f"{prev_model.__name__} не имеет атрибута '{attr_name}'"
                )

            attr = getattr(prev_model, attr_name)

            if current_load is None:
                current_load = selectinload(attr)
            else:
                current_load = current_load.selectinload(attr)

            prev_model = next_model

        if current_load is not None:
            stmt = stmt.options(current_load)

        result = await self.session.execute(stmt)
        return result.scalars().unique().all()

    async def get_all_by_field(self, field: str, value: Any) -> Sequence[T]:
        """
        Получает все записи по любому полю.

        Получает все записи, соответствующие значению указанного поля.

        Используется для выборки по полям: `user_id`, `status`, `is_active` и т.д.

        Args:
            field (str): Название поля модели (например: "email", "status", "user_id")
            value (Any): Значение для поиска (например: "Tom", "tom@email.com", 123)

        Raises:
            ValueError: Если указанное поле отсутствует в модели

        Returns:
            Sequence[T]: Список экземпляров модели (может быть пустым)
        """
        if not hasattr(self.model_db, field):
            raise ValueError(f"Модель {self.model_db.__name__} не имеет поля '{field}'")

        stmt = select(self.model_db).where(getattr(self.model_db, field) == value)  # type: ignore
        result = await self.session.execute(stmt)
        return result.scalars().unique().all()

    async def get_by_fields(self, **filters) -> Sequence[T]:
        """
        Получает все записи, соответствующие нескольким полям и значениям.

        Выполняет фильтрацию по любому количеству полей.

        Используется для сложных выборок: например, заказы с определённым статусом и пользователем.

        Args:
            **filters: Пары "поле=значение" для фильтрации (например: status="paid", user_id=5)

        Raises:
            ValueError: Если одно из указанных полей отсутствует в модели

        Returns:
            Sequence[T]: Список экземпляров модели, соответствующих всем условиям
        """
        stmt = select(self.model_db)
        for field, value in filters.items():
            if not hasattr(self.model_db, field):
                raise ValueError(
                    f"Модель {self.model_db.__name__} не имеет поля '{field}'"
                )
            stmt = stmt.where(getattr(self.model_db, field) == value)  # type: ignore
        result = await self.session.execute(stmt)
        return result.scalars().unique().all()

    async def get_all(self) -> Sequence[T]:
        """
        Получает все записи указанной модели.

        Returns:
            Sequence[T]: Список всех экземпляров модели (может быть пустым)
        """
        stmt = select(self.model_db)
        result = await self.session.execute(stmt)
        return result.scalars().unique().all()

    async def update(self, instance: T, data) -> T:
        """
        Обновляет существующую запись в базе данных.

        Поддерживает частичное обновление (`exclude_unset=True`), что позволяет обновлять только указанные поля.

        Args:
            instance (T): Существующий экземпляр модели
            data: Pydantic-схема с новыми данными

        Returns:
            T: Обновлённый экземпляр модели
        """
        for name, value in data.model_dump(exclude_unset=True).items():
            setattr(instance, name, value)
        await self.session.commit()
        return instance

    async def delete(self, instance: T) -> bool:
        """
        Удаляет запись из базы данных.

        Args:
            instance (T): Экземпляр модели, который нужно удалить

        Returns:
            bool: Всегда `True`, если удаление прошло успешно
        """
        await self.session.delete(instance)
        await self.session.commit()
        return True
