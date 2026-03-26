from fastapi import Request
from starlette.datastructures import MutableHeaders
from starlette.middleware.base import BaseHTTPMiddleware

from core.config import settings


class SecurityHeadersMiddleware(BaseHTTPMiddleware):
    """
    Middleware для установки безопасности HTTP-заголовков.

    Назначение:
    -----------
    Этот модуль содержит `SecurityHeadersMiddleware` — middleware для FastAPI, который автоматически добавляет
    набор HTTP-заголовков безопасности ко всем исходящим ответам. Это помогает защитить приложение от
    распространённых веб-угроз, таких как XSS, кликджекинг, MIME-сниффинг и др.

    Используется как часть общего подхода к безопасности на уровне HTTP.

    Заголовки, которые устанавливаются:
    -----------------------------------
    - `X-Content-Type-Options: nosniff` — запрещает браузеру определять MIME-тип по содержимому, предотвращая
      атаки через поддельные типы (например, выполнение JS из файла, выдаваемого за изображение).

    - `X-Frame-Options: DENY` — запрещает встраивание страницы в `<frame>`, `<iframe>`, `<object>`, защищая
      от атак типа clickjacking.

    - `X-XSS-Protection: 1; mode=block` — включает встроенный XSS-фильтр в старых браузерах (устаревший,
      но полезен для совместимости).

    - `Referrer-Policy: no-referrer` — ограничивает передачу информации о refer, повышая приватность.

    - `Permissions-Policy` — отключает доступ к чувствительным API (геолокация, камера, микрофон), если
      они не требуются.

    - `Strict-Transport-Security` (HSTS) — включается **только в продакшене** (не на localhost), требует
      использование HTTPS и предотвращает downgrade-атаки.

    Условия включения HSTS:
    -----------------------
    - Включается только если `settings.run.host` не является `127.0.0.1` или `localhost`.
    - Рекомендуется использовать только при работе с HTTPS (в продакшене).

    Пример:
    -------
    Если приложение запущено на `localhost`, HSTS не будет добавлен. На сервере — будет HSTS.

    Использование:
    --------------
    Добавляется в приложение через `app.add_middleware(SecurityHeadersMiddleware)`
    """

    async def dispatch(self, request: Request, call_next):
        response = await call_next(request)

        headers = {
            "X-Content-Type-Options": "nosniff",
            "X-Frame-Options": "DENY",
            "X-XSS-Protection": "1; mode=block",
            "Referrer-Policy": "no-referrer",
            "Permissions-Policy": "geolocation=(), microphone=(), camera=()",
        }

        # Добавляем HSTS только в продакшене (HTTPS)
        if (
            not settings.run.host == "127.0.0.1"
            and not settings.run.host == "localhost"
        ):
            headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"

        response_headers = MutableHeaders(headers=response.headers)
        for key, value in headers.items():
            if key not in response_headers:
                response_headers[key] = value
        return response
