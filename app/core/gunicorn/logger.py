from logging import Formatter
from gunicorn.glogging import Logger

from core.config import settings


class GunicornLogger(Logger):
    """
    Кастомный логер для Gunicorn с единым форматом логов.

    Заменяет стандартный логер Gunicorn, чтобы:
        - Использовать единый формат логов (`settings.logging.log_format`)
        - Централизовать вывод в stdout
        - Синхронизировать логи с основным приложением

    Attributes:
        access_log: Лог доступа (HTTP-запросы)
        error_log: Лог ошибок (критические события, исключения)
    """

    def setup(self, cfg) -> None:
        """
        Настраивает обработчики логов для access и error логов.

        Применяет единый формат из `settings.logging.log_format`.

        Args:
            cfg: Конфигурация Gunicorn (передаётся автоматически)
        """
        super().setup(cfg)

        self._set_handler(
            log=self.access_log,
            output=cfg.accesslog,
            fmt=Formatter(fmt=settings.logging.log_format),
        )
        self._set_handler(
            log=self.error_log,
            output=cfg.errorlog,
            fmt=Formatter(fmt=settings.logging.log_format),
        )
