<p align="center">
  <a href="README.en.md">English</a> | <b>Русский</b>
</p>

---

# ![Логотип приложения](docs/assets/logo.png) FastH-Core-Stack

**FastH-Core-Stack** — это высокопроизводительный `Fullstack-boilerplate`, спроектированный для быстрой разработки 
асинхронных и защищенных веб-приложений. 

Это готовый «фундамент» на базе `Clean Architecture`, где вся базовая инфраструктура — 
от Full Auth Lifecycle, админки, Docker-окружения до интерактивного UI — уже настроена и работает «из коробки». 
Забудь про тяжелые JS-фреймворки и настройку JWT: здесь всё работает на мощи `FastAPI` и гибкости `HTMX`, 
обеспечивая `SPA`-опыт на чистом `Python`.

**Этот шаблон позволяет вам сосредоточиться на реализации бизнес-идей с первых минут.**

![Изображения стека](docs/assets/technology-stack.jpg)

## 📚 Содержание
- [🛠️ Технологический стек](#-технологический-стек)
- [✅ Функционал](#-функционал)
- [📂 Структура проекта](#-структура-проекта)
- [📸 Примеры работы приложения](#-примеры-работы-приложения)
- [⚙️ Установка и запуск](#-установка-и-запуск)
- [📬 Контакты](#-контакты)

## 🛠️ Технологический стек

| Компоненты | |
|----------|---:|
| **🐍 Язык:** Python 3.14+ | [![Python](https://img.shields.io/badge/Python-3.14%2B-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/) |
| **⚡ Фреймворк:** FastAPI | [![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/) |
| **🪄 Фронтенд:** HTMX | [![HTMX](https://img.shields.io/badge/HTMX-06204f?style=for-the-badge&logo=htmx&logoColor=white)](https://htmx.org) |
| **📅 Планировщик:** APScheduler | [![APScheduler](https://img.shields.io/badge/APScheduler-black?style=for-the-badge&logo=python&logoColor=white)](https://readthedocs.io) |
| **🚀 ASGI-сервер:** Uvicorn + Gunicorn | [![Uvicorn](https://img.shields.io/badge/Uvicorn-005571?style=for-the-badge&logo=fastapi&logoColor=white)](https://www.uvicorn.org/) [![Gunicorn](https://img.shields.io/badge/Gunicorn-F46D43?style=for-the-badge&logo=apache&logoColor=white)](https://gunicorn.org/) |
| **🗄️ База Данных:** PostgreSQL (asyncpg) | [![PostgreSQL](https://img.shields.io/badge/PostgreSQL-316192?style=for-the-badge&logo=postgresql&logoColor=white)](https://www.postgresql.org/) |
| **🔁 ORM:** SQLAlchemy (async) | [![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-0B5566?style=for-the-badge&logo=python&logoColor=white)](https://www.sqlalchemy.org/) |
| **🔄 Миграции БД:** Alembic | [![Alembic](https://img.shields.io/badge/Alembic-0B5566?style=for-the-badge&logo=python&logoColor=white)](https://alembic.sqlalchemy.org/) |
| **🔐 Аутентификация:** FastAPI-Users | [![FastAPI-Users](https://img.shields.io/badge/FastAPI--Users-005571?style=for-the-badge&logo=fastapi&logoColor=white)](https://fastapi-users.github.io/fastapi-users/) |
| **🔧 Админка:** SQLAdmin | [![SQLAdmin](https://img.shields.io/badge/SQLAdmin-0B5566?style=for-the-badge&logo=python&logoColor=white)](https://aminalaee.dev/sqladmin/) |
| **✅ Валидация:** Pydantic v2 + pydantic-settings | [![Pydantic](https://img.shields.io/badge/Pydantic-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://docs.pydantic.dev/) [![pydantic--settings](https://img.shields.io/badge/pydantic--settings-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://docs.pydantic.dev/latest/concepts/pydantic_settings/) |
| **🧩 Кэширование:** Redis + fastapi-cache2 | [![Redis](https://img.shields.io/badge/Redis-DC382D?style=for-the-badge&logo=redis&logoColor=white)](https://redis.io/) |
| **📄 Шаблонизация:** Jinja2 | [![Jinja2](https://img.shields.io/badge/Jinja2-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://jinja.palletsprojects.com/) |
| **🛡️ Защита:** slowapi + CORS | [![slowapi](https://img.shields.io/badge/slowapi-005571?style=for-the-badge&logo=fastapi&logoColor=white)](https://slowapi.readthedocs.io/) [![CORS](https://img.shields.io/badge/CORS-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://fastapi.tiangolo.com/tutorial/cors/) |
| **📧 Почта:** aiosmtplib | [![aiosmtplib](https://img.shields.io/badge/aiosmtplib-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://aiosmtplib.readthedocs.io/) |
| **📦 Менеджер пакетов:** uv | [![uv](https://img.shields.io/badge/uv-000000?style=for-the-badge&logo=python&logoColor=white)](https://docs.astral.sh/uv/) |
| **🐳 Контейнеризация:** Docker + Docker Compose | [![Docker](https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white)](https://www.docker.com/) [![Docker Compose](https://img.shields.io/badge/Docker_Compose-2496ED?style=for-the-badge&logo=docker&logoColor=white)](https://docs.docker.com/compose/) |
| **🧪 Тестирование:** Pytest + httpx + faker | [![Pytest](https://img.shields.io/badge/Pytest-0A9EDC?style=for-the-badge&logo=pytest&logoColor=white)](https://docs.pytest.org/) [![HTTPX](https://img.shields.io/badge/HTTPX-0A9EDC?style=for-the-badge&logo=python&logoColor=white)](https://www.python-httpx.org/) [![Faker](https://img.shields.io/badge/Faker-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://faker.readthedocs.io/) |
| **📘 Документация:** OpenAPI (Swagger UI) | [![OpenAPI](https://img.shields.io/badge/OpenAPI-10985B?style=for-the-badge&logo=swagger&logoColor=white)](https://swagger.io/specification/) |
| **🧹 Форматирование кода:** Black | [![Black](https://img.shields.io/badge/Code%20Style-Black-000000?style=for-the-badge&logo=python&logoColor=white)](https://black.readthedocs.io/) |
| **📊 Покрытие тестами:** pytest-cov | [![pytest-cov](https://img.shields.io/badge/pytest--cov-0A9EDC?style=for-the-badge&logo=pytest&logoColor=white)](https://pytest-cov.readthedocs.io/) |

## ✅ Функционал

- **🔐 Полный цикл Auth & Security (FastAPI-Users)**
  > Готовая логика регистрации, входа, верификации email и восстановления пароля. Поддержка сессий на базе БД с 
  > безопасными `HTTP-only куками`.
- **🪄 Интерактивный UI (HTMX + Jinja2)**
  > `SPA`-опыт без использования тяжелых JS-фреймворков. Динамическая подгрузка контента, обработка форм и обновление 
  > компонентов без перезагрузки страницы.
- **💎 Дизайн в стиле Glassmorphism**
  > Современный «воздушный» интерфейс с эффектами матового стекла, адаптивной версткой и встроенными индикаторами 
  > загрузки (preloaders) для лучшего `UX`.
- **🧹 Автоматическая гигиена БД (APScheduler)**
  > Встроенный фоновый планировщик задач, который автоматически очищает просроченные токены и удаляет неподтвержденные 
  > аккаунты, поддерживая базу данных в чистоте.
- **🛠️ Профессиональная админ-панель (SQLAdmin)**
  > Полноценный интерфейс для управления данными: CRUD операции, поиск и фильтрация. 
  > Настроено красивое отображение дат и статусов пользователей.
- **🛡️ Защита и контроль трафика (Slowapi)**
  > Встроенный `Rate Limiting` на критических эндпоинтах для защиты от brute-force и спама. 
  > Гибкая настройка CORS для безопасности.
- **🏗️ Современная архитектура (Clean Architecture)**
  > Четкое разделение на слои: API, Views, Services, Repositories и Models.
  > Проект спроектирован как надежный и масштабируемый фундамент.
- **🚀 Высокая производительность (uv + orjson)**
  > Использование пакетного менеджера `uv` для мгновенной установки зависимостей и сборки Docker-образов.
  > Ультра-быстрая сериализация данных через `orjson`.
- **🗄️ Асинхронная работа с данными (SQLAlchemy 2.0)**
  > Полностью асинхронное взаимодействие с `PostgreSQL` через `asyncpg`.
  > Универсальный базовый репозиторий для минимизации шаблонного кода при работе с БД.
- **🔄 Автоматизация миграций (Alembic)**
  > Управление схемами базы данных с поддержкой асинхронности.
  > Автоматический накат миграций при запуске контейнера.
- **📧 Асинхронные уведомления (aiosmtplib)**
  > Отправка системных и транзакционных писем (подтверждение регистрации, сброс пароля) без блокировки основного потока приложения.
- **🧩 Кэширование (Redis + fastapi-cache2)**
  > Интеграция с `Redis` для кэширования тяжелых запросов, что значительно снижает нагрузку на базу данных и ускоряет отклик API.
- **📦 Контейнеризация и DevOps (Docker)**
  > Готовая инфраструктура в `Docker Compose`: приложение, БД, Redis и PGAdmin запускаются одной командой.
  > Поддержка `Hot Reload` для быстрой разработки внутри контейнера через watch.
- **🧪 Надежное тестирование (Pytest)**
  > Настроенная среда для тестирования асинхронного API с использованием `HTTPX`.
  > Генерация фейковых данных через `Faker` и отчеты о покрытии кода через `pytest-cov`.
- **📘 Автодокументация (Swagger)**
  > Всегда актуальная интерактивная документация API по стандартам `OpenAPI`, доступная по адресу `/docs`.

## 📂 Структура проекта

```bash
FastH-Core-Stack/
├── app/                         # Основной пакет приложения
│   ├── actions/                 # CLI-скрипты управления (создание суперпользователя и др.)
│   ├── admin/                   # Конфигурация админ-панели SQLAdmin
│   ├── alembic/                 # История и версии миграций базы данных
│   ├── api/                     # Слой сетевых интерфейсов (API)
│   │   ├── api_v1/              # Первая версия REST API эндпоинтов
│   │   ├── dependencies/        # Инъекции зависимостей (Depends) для роутеров
│   │   ├── webhooks/            # Обработчики входящих уведомлений от внешних систем
│   │   └── __init__.py          # Агрегация и инициализация роутеров
│   ├── core/                    # Системное ядро и инфраструктурные компоненты
│   │   ├── auth/                # Конфигурация безопасности и логика fastapi-users
│   │   ├── cache/               # Настройки и утилиты кэширования (Redis)
│   │   ├── gunicorn/            # Конфигурация WSGI-сервера для продакшена
│   │   ├── config.py            # Валидация настроек через pydantic-settings (.env)
│   │   ├── db_helper.py         # Инициализация движка SQLAlchemy и сессий
│   │   ├── limiter.py           # Настройка ограничений частоты запросов (Rate Limiting)
│   │   └── templates.py         # Интеграция и конфигурация Jinja2Templates
│   ├── exceptions/              # Обработка исключений
│   │   ├── custom.py            # Определение пользовательских классов ошибок
│   │   └── handlers.py          # Глобальные обработчики исключений
│   ├── middleware/              # Кастомные middleware
│   ├── models/                  # Описание сущностей базы данных (ORM SQLAlchemy)
│   ├── repositories/            # Слой доступа к данным (Data Access Layer)
│   │   └── crud_manager.py      # Универсальный CRUD-менеджер для работы с моделями
│   ├── schemas/                 # Модели данных Pydantic (DTO) для валидации
│   ├── services/                # Слой бизнес-логики (UseCase Layer)
│   │   └── mailing/             # Почтовый сервис (рассылка уведомлений, подтверждений)
│   ├── static/                  # Статическое содержимое (CSS, JS, Изображения)
│   ├── templates/               # HTML-шаблоны с HTMX и Jinja2
│   ├── utils/                   # Вспомогательные функции общего назначения
│   │   └── case_converter.py    # Функция конвертации имени таблицы
│   ├── views/                   # Роутеры для рендеринга HTML-страниц и HTMX-форм (Frontend-интерфейс)
│   ├── .env                     # Переменные окружения (не отображается в git)
│   ├── .env.template            # Шаблон .env (автоматически заменяет .env, если его нет)
│   ├── alembic.ini              # Конфигурационный файл миграций Alembic
│   ├── create_fastapi_app.py    # Фабрика для сборки и настройки экземпляра FastAPI 
│   ├── main.py                  # Точка входа для запуска в режиме разработки
│   ├── run.py                   # Запуск приложения через Gunicorn (для Docker)
│   └── run_main.py              # Создания и запуск приложения через Gunicorn
├── docker-build/                # Инфраструктурные файлы сборки
│   └── app/
│       ├── Dockerfile           # Инструкции для сборки Docker-образа
│       └── prestart.sh          # Скрипт подготовки БД (миграции + создание админа)
├── tests/                       # Пакет с автоматизированными тестами (Pytest)
├── docker-compose.yml           # Оркестрация контейнеров (App, DB, Redis, PGAdmin)
├── pyproject.toml               # Конфигурация проекта, зависимостей и инструментов (uv)
└── uv.lock                      # Фиксированные версии установленных пакетов
```

## 📸 Примеры работы приложения

### 🖼️ Интерфейс и возможности (Showcase)

Ниже представлены ключевые экраны приложения, демонстрирующие интеграцию **FastAPI**, **HTMX** и современный **Glassmorphism UI**:

- `🏠 Main Hub` — Главная страница с адаптивной версткой, готовым футером и навигацией.
- `🔐 Auth Lifecycle` — Полноценный цикл регистрации, входа и восстановления пароля через «Забыл пароль».
- `📧 Email Verification` — Автоматические страницы уведомлений об успешном или неудачном подтверждении почты.
- `👤 User Profile` — Личный кабинет пользователя с управлением данными профиля.
- `🛡️ Security & Access` — Форма смены пароля и страницы безопасности (правила сайта).
- `🛠️ Admin Control ` — Профессиональный интерфейс управления данными (на базе SQLAdmin) для полного контроля над БД.
- `🚦 Error Handling` — Кастомные страницы для обработки системных событий:
  - `404 Not Found` — Если страница не существует.
  - `429 Rate Limit` — Интеллектуальная защита от перегрузок и ботов (Slowapi).

> *Все формы работают асинхронно через HTMX, обеспечивая мгновенный отклик без перезагрузки страниц.*

![Изображения работы приложения](docs/assets/examples-application-operation.png)

## ⚙️ Установка и запуск

1. **Клонируйте репозиторий**
> В терминале выполните команду:
> ```bash
> git clone https://github.com/Mishchenko-Vladimir/FastH-Core-Stack.git
> ```
> Перейдите в директорию проекта:
> ```bash
> cd FastH-Core-Stack
> ```

2. **Настройка переменных окружения**
> Заполните файлы `.env.template` и `docker-compose.yml` своими значениями.

3. **Ваша разработка и настройка приложения**
> Синхронизируйте виртуальное окружение проекта с зависимостями:
> ```bash
> uv sync
> ```
> Примените миграцию:
> ```bash
> cd app
> alembic upgrade head
> cd ..
> ```
> Просто редактируйте и добавляйте новые файлы в папку `app/`, и изменения автоматически применятся в запущенном контейнере.
>
> Локальный запуск (без `Docker`):
> ```bash
> uv run python app/main.py
> ```

4. **Запуск приложение через Docker**
> Если вы запускаете образ в Windows, убедись что файлы `docker-build/app/prestart.sh` и `app/run.py`, стоят в расширении `LF`, а не `CRLF`.
> 
> Сборка образа с именем `app`:
> ```bash
> docker compose build app
> ```
> Запуск сборки (приложения):
> ```bash
> docker compose up -d
> ```
> Остальные команды `docker`:
> - `docker compose ps` — посмотреть какие контейнеры запущены
> - `docker compose logs -f app` — посмотреть логи приложения
> - `docker compose stop` — остановка приложения
> - `docker compose down` — удаления сборки

> Приложение будет доступно по адресу http://localhost:8000, а документация http://localhost:8000/docs 

## 📬 Контакты

### 💻 Автор: Мищенко Владимир
- **GitHub:** [Mishchenko-Vladimir](https://github.com/Mishchenko-Vladimir)
- **Mail.ru:** [mishchienko.2001@mail.ru](mailto:mishchienko.2001@mail.ru)
- **Gmail:** [mishchieko.2001@gmail.com](mailto:mishchieko.2001@gmail.com)
- **Telegram:** [@VM_Dev](https://t.me/VM_Dev)

💌 Не забудьте поставить звезду ⭐ на GitHub, если вам понравился проект! 😉

---
[↑ Вернуться наверх](#-fastAPI-boilerplate)
