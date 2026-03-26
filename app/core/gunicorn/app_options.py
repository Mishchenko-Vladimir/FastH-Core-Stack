from .logger import GunicornLogger


def get_app_options(
    host: str,
    port: int,
    timeout: int,
    workers: int,
    log_level: str,
) -> dict:
    """
    Возвращает стандартные опции для запуска Gunicorn с FastAPI.

    Args:
        host (str): Хост (например, "127.0.0.1")
        port (int): Порт (например, 8000)
        timeout (int): Таймаут в секундах
        workers (int): Количество воркеров
        log_level (str): Уровень логирования ("info", "debug", "warning")

    Returns:
        dict: Готовый словарь опций для Gunicorn
    """
    return {
        "accesslog": "-",  # Вывод в stdout
        "errorlog": "-",  # Вывод в stdout
        "bind": f"{host}:{port}",  # Адрес привязки
        "loglevel": log_level,  # Уровень логов
        "logger_class": GunicornLogger,  # Кастомный логер
        "timeout": timeout,  # Таймаут обработки запроса
        "workers": workers,  # Количество воркеров
        "worker_class": "uvicorn.workers.UvicornWorker",  # Асинхронный воркер
    }
