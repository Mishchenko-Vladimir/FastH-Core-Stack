from fastapi import FastAPI
from gunicorn.app.base import BaseApplication


class Application(BaseApplication):
    """
    Адаптер для запуска FastAPI-приложения через Gunicorn.

    Позволяет использовать Gunicorn как WSGI-сервер с UvicornWorker,
    что даёт возможность запускать асинхронное приложение с несколькими воркерами.

    Пример использования:
        app = FastAPI()
        options = get_app_options(...)
        Application(app, options).run()

    Attributes:
        application (FastAPI): Экземпляр FastAPI-приложения
        options (dict): Конфигурационные параметры Gunicorn

    Args:
        application (FastAPI): Экземпляр FastAPI
        options (dict | None): Опции Gunicorn (host, port, workers и т.д.)
    """

    def __init__(self, application: FastAPI, options: dict | None = None):
        self.options = options or {}
        self.application = application
        super().__init__()

    def load(self):
        """
        Возвращает WSGI-приложение.

        Вызывается Gunicorn при старте.

        Returns:
            FastAPI: Приложение, готовое к обработке запросов
        """
        return self.application

    @property
    def config_options(self) -> dict:
        """
        Проверяет есть ли ключ.

        Returns:
            dict: Валидные настройки для Gunicorn
        """
        return {
            k: v
            for k, v in self.options.items()
            if k in self.cfg.settings and v is not None
        }

    def load_config(self):
        """
        Применяет конфигурацию к Gunicorn.

        Устанавливает параметры (например, bind, workers) через `self.cfg.set()`.
        """
        for key, value in self.config_options.items():
            self.cfg.set(key.lower(), value)
