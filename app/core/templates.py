from fastapi.templating import Jinja2Templates
from datetime import datetime

from core.config import BASE_DIR


def format_datetime(value: str | datetime) -> str:
    """
    Преобразует строку или объект datetime в форматированную строку 'ГГГГ-ММ-ДД ЧЧ:ММ'.

    Поддерживает:
    - Объекты `datetime.datetime`
    - ISO-форматированные строки (например: '2025-10-07T12:25:49.158480' или '2025-10-07T12:25:49.158480+00:00')
    - Автоматическое удаление 'Z' (обозначение UTC) для корректного парсинга.

    Используется как фильтр в Jinja2:
        {{ user.created_at | format_datetime }}

    Args:
        value (str | datetime): Дата в виде строки ISO или объекта datetime.

    Returns:
        str: Отформатированная строка в формате 'ГГГГ-ММ-ДД ЧЧ:ММ', или исходное значение при ошибке.
    """
    if isinstance(value, str):
        try:
            # Пробуем преобразовать строку в datetime
            dt = datetime.fromisoformat(value.replace("Z", "+00:00"))
        except ValueError:
            return value  # Возвращаем исходную строку, если не удалось преобразовать
    elif isinstance(value, datetime):
        dt = value
    else:
        return ""

    return dt.strftime("%Y-%m-%d %H:%M")


class AppTemplates(Jinja2Templates):
    """Добавляет дополнительные фильтры для шаблонов Jinja2Templates."""

    def __init__(self, directory):
        super().__init__(directory=directory)
        self.env.filters["format_datetime"] = format_datetime


templates = AppTemplates(directory=BASE_DIR / "templates")
