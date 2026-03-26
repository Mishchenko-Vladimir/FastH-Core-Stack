import logging

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import ORJSONResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.docs import (
    get_redoc_html,
    get_swagger_ui_html,
    get_swagger_ui_oauth2_redirect_html,
)
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend

from sqladmin import Admin
from slowapi.middleware import SlowAPIMiddleware
from contextlib import asynccontextmanager
from redis.asyncio import Redis

from admin import register_admin_views
from admin.admin_auth import AdminAuth

from middleware.custom_rate_limit_middleware import CustomRateLimitMiddleware
from middleware.security_headers_middleware import SecurityHeadersMiddleware

from api.webhooks import webhooks_router
from core import db_helper, limiter, settings, BASE_DIR
from core.auth.tasks import setup_auth_scheduler
from exceptions.handlers import register_errors_handlers

log = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Управление жизненным циклом приложения (lifespan).
    Выполняется при старте и завершении приложения.

    :param app: Экземпляр FastAPI приложения.
    :yields: Ничего не возвращает, передаёт управление приложению.
    :side effects:
        - Инициализирует базу данных.
        - Инициализирует кэш через Redis.
        - Инициализирует планировщик задач для Auth.
        - Останавливает планировщик задач при завершении.
        - Закрывает соединение с БД при завершении.
    """
    # startup (старт приложения)
    if settings.site.environment != "testing":
        if settings.cache.enabled:
            redis = Redis(
                host=settings.redis.host,
                port=settings.redis.port,
                db=settings.redis.db.cache,
            )
            FastAPICache.init(
                RedisBackend(redis),
                prefix=settings.cache.prefix,
            )
            log.info("Кэширование ВКЛЮЧЕНО")
        else:
            log.info("Кэширование ОТКЛЮЧЕНО")

    # Инициализация планировщика задач Auth
    auth_scheduler = setup_auth_scheduler()
    auth_scheduler.start()

    yield
    # shutdown (завершение приложения)
    auth_scheduler.shutdown()
    await db_helper.dispose()  # Закрытия бд


def register_static_docs_routes(app: FastAPI):
    """
    Создание статических URL для Swagger, ReDoc и статических файлов.
    Необходимо для того, чтобы документация нормально открывалась.

    :param app: Экземпляр FastAPI приложения.
    :side effects:
        - Добавляет ручки:
          - `/docs` → кастомный Swagger UI
          - `/redoc` → кастомный ReDoc
          - `/docs/oauth2-redirect` → редирект для OAuth2
    :notes:
        - Используется, если `create_custom_static_urls=True`
        - Позволяет обновлять UI без перезапуска приложения
    """

    @app.get("/docs", include_in_schema=False)
    async def custom_swagger_ui_html():
        return get_swagger_ui_html(
            openapi_url=app.openapi_url,
            title=app.title + " - Swagger UI",
            oauth2_redirect_url=app.swagger_ui_oauth2_redirect_url,
            swagger_js_url="https://unpkg.com/swagger-ui-dist@5/swagger-ui-bundle.js",
            swagger_css_url="https://unpkg.com/swagger-ui-dist@5/swagger-ui.css",
        )

    @app.get(app.swagger_ui_oauth2_redirect_url, include_in_schema=False)
    async def swagger_ui_redirect():
        return get_swagger_ui_oauth2_redirect_html()

    @app.get("/redoc", include_in_schema=False)
    async def redoc_html():
        return get_redoc_html(
            openapi_url=app.openapi_url,
            title=app.title + " - ReDoc",
            redoc_js_url="https://unpkg.com/redoc@next/bundles/redoc.standalone.js",
        )


def create_app(
    create_custom_static_urls: bool = False,
    lifespan_override=None,
) -> FastAPI:
    """
    Фабрика для создания экземпляра FastAPI приложения.

    :param create_custom_static_urls: True — отключает стандартные /docs и /redoc, и регистрирует кастомные с CDN.
    :param lifespan_override: Возможность переопределить функцию lifespan (для тестов).
    :return: Настроенный экземпляр FastAPI.
    :side effects:
        - Добавляет middleware:
          - CORS
          - Rate Limiting (SlowAPI + Custom)
          - Security Headers
        - Добавление SQLAdmin
        - Монтирует статику (/static)
        - Регистрирует обработчики ошибок
        - Подключает вебхуки
    """

    app = FastAPI(
        default_response_class=ORJSONResponse,
        lifespan=lifespan_override or lifespan,
        docs_url=None if create_custom_static_urls else "/docs",
        redoc_url=None if create_custom_static_urls else "/redoc",
        webhooks=webhooks_router,
    )

    # Защита от bruteforce и DDoS.
    if settings.rate_limit.enabled and settings.site.environment != "testing":
        app.state.limiter = limiter  # type: ignore
        app.add_middleware(SlowAPIMiddleware)
        app.add_middleware(CustomRateLimitMiddleware)

    # Установка безопасности HTTP-заголовков.
    app.add_middleware(SecurityHeadersMiddleware)

    # Добавления и настройка CORS.
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.site.allowed_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    if settings.site.environment != "testing":
        authentication_backend = AdminAuth(
            secret_key=settings.access_token.verification_token_secret
        )
        admin = Admin(
            app=app,
            session_maker=db_helper.session_factory,
            authentication_backend=authentication_backend,
        )
        register_admin_views(admin)

    # Создание статических URL для Swagger, ReDoc.
    if create_custom_static_urls:
        register_static_docs_routes(app)

    # Регистрация статических файлов в папке static.
    app.mount("/static", StaticFiles(directory=BASE_DIR / "static"), name="static")

    # Регистрация обработчиков ошибок(404, 500 и др.) из модуля errors_handlers
    register_errors_handlers(app)
    return app
