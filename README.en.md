<p align="center">
  <b>English</b> | <a href="../../">Русский</a>
</p>

---

# ![Application Logo](docs/assets/logo.png) FastH-Core-Stack

**FastH-Core-Stack** is a high-performance `Fullstack boilerplate` designed for the rapid development of 
asynchronous and secure web applications.

It provides a production-ready foundation based on `Clean Architecture`, where the entire core infrastructure — from a 
Full Auth Lifecycle, Admin Panel, and Docker environment to an interactive UI — is already pre-configured and works "out of the box." 
Forget about heavy JS frameworks and JWT overhead: everything here is powered by `FastAPI` and `HTMX`, delivering a seamless `SPA experience` using pure `Python`.

**This template allows you to focus on implementing your business ideas from the very first minute.**

![Technology Stack](docs/assets/technology-stack.jpg)

## 📚 Table of Contents
- [🛠️ Tech Stack](#-tech-stack)
- [✅ Features](#-features)
- [📂 Project Structure](#-project-structure)
- [⚙️ Installation and Setup](#-installation-and-setup)
- [📬 Contacts](#-contacts)

## 🛠️ Tech Stack

| Components | |
|----------|---:|
| **🐍 Language:** Python 3.14+ | [![Python](https://img.shields.io/badge/Python-3.14%2B-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/) |
| **⚡ Framework:** FastAPI | [![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/) |
| **🪄 Frontend:** HTMX | [![HTMX](https://img.shields.io/badge/HTMX-06204f?style=for-the-badge&logo=htmx&logoColor=white)](https://htmx.org) |
| **📅 Scheduler:** APScheduler | [![APScheduler](https://img.shields.io/badge/APScheduler-black?style=for-the-badge&logo=python&logoColor=white)](https://readthedocs.io) |
| **🚀 ASGI Server:** Uvicorn + Gunicorn | [![Uvicorn](https://img.shields.io/badge/Uvicorn-005571?style=for-the-badge&logo=fastapi&logoColor=white)](https://www.uvicorn.org/) [![Gunicorn](https://img.shields.io/badge/Gunicorn-F46D43?style=for-the-badge&logo=apache&logoColor=white)](https://gunicorn.org/) |
| **🗄️ Database:** PostgreSQL (asyncpg) | [![PostgreSQL](https://img.shields.io/badge/PostgreSQL-316192?style=for-the-badge&logo=postgresql&logoColor=white)](https://www.postgresql.org/) |
| **🔁 ORM:** SQLAlchemy (async) | [![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-0B5566?style=for-the-badge&logo=python&logoColor=white)](https://www.sqlalchemy.org/) |
| **🔄 DB Migrations:** Alembic | [![Alembic](https://img.shields.io/badge/Alembic-0B5566?style=for-the-badge&logo=python&logoColor=white)](https://alembic.sqlalchemy.org/) |
| **🔐 Authentication:** FastAPI-Users | [![FastAPI-Users](https://img.shields.io/badge/FastAPI--Users-005571?style=for-the-badge&logo=fastapi&logoColor=white)](https://fastapi-users.github.io/fastapi-users/) |
| **🔧 Admin Panel:** SQLAdmin | [![SQLAdmin](https://img.shields.io/badge/SQLAdmin-0B5566?style=for-the-badge&logo=python&logoColor=white)](https://aminalaee.dev/sqladmin/) |
| **✅ Validation:** Pydantic v2 + pydantic-settings | [![Pydantic](https://img.shields.io/badge/Pydantic-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://docs.pydantic.dev/) [![pydantic--settings](https://img.shields.io/badge/pydantic--settings-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://docs.pydantic.dev/latest/concepts/pydantic_settings/) |
| **🧩 Caching:** Redis + fastapi-cache2 | [![Redis](https://img.shields.io/badge/Redis-DC382D?style=for-the-badge&logo=redis&logoColor=white)](https://redis.io/) |
| **📄 Templating:** Jinja2 | [![Jinja2](https://img.shields.io/badge/Jinja2-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://jinja.palletsprojects.com/) |
| **🛡️ Security:** slowapi + CORS | [![slowapi](https://img.shields.io/badge/slowapi-005571?style=for-the-badge&logo=fastapi&logoColor=white)](https://slowapi.readthedocs.io/) [![CORS](https://img.shields.io/badge/CORS-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://fastapi.tiangolo.com/tutorial/cors/) |
| **📧 Email:** aiosmtplib | [![aiosmtplib](https://img.shields.io/badge/aiosmtplib-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://aiosmtplib.readthedocs.io/) |
| **📦 Package Manager:** uv | [![uv](https://img.shields.io/badge/uv-000000?style=for-the-badge&logo=python&logoColor=white)](https://docs.astral.sh/uv/) |
| **🐳 Containerization:** Docker + Docker Compose | [![Docker](https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white)](https://www.docker.com/) [![Docker Compose](https://img.shields.io/badge/Docker_Compose-2496ED?style=for-the-badge&logo=docker&logoColor=white)](https://docs.docker.com/compose/) |
| **🧪 Testing:** Pytest + httpx + faker | [![Pytest](https://img.shields.io/badge/Pytest-0A9EDC?style=for-the-badge&logo=pytest&logoColor=white)](https://docs.pytest.org/) [![HTTPX](https://img.shields.io/badge/HTTPX-0A9EDC?style=for-the-badge&logo=python&logoColor=white)](https://www.python-httpx.org/) [![Faker](https://img.shields.io/badge/Faker-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://faker.readthedocs.io/) |
| **📘 Documentation:** OpenAPI (Swagger UI) | [![OpenAPI](https://img.shields.io/badge/OpenAPI-10985B?style=for-the-badge&logo=swagger&logoColor=white)](https://swagger.io/specification/) |
| **🧹 Code Formatting:** Black | [![Black](https://img.shields.io/badge/Code%20Style-Black-000000?style=for-the-badge&logo=python&logoColor=white)](https://black.readthedocs.io/) |
| **📊 Test Coverage:** pytest-cov | [![pytest-cov](https://img.shields.io/badge/pytest--cov-0A9EDC?style=for-the-badge&logo=pytest&logoColor=white)](https://pytest-cov.readthedocs.io/) |

## ✅ Features

- **🔐 Full Auth & Security Lifecycle (FastAPI-Users)**
  > Ready-to-use logic for registration, login, email verification, and password recovery. 
  > Supports database-backed sessions with secure `HTTP-only cookies`.
- **🪄 Interactive UI (HTMX + Jinja2)**
  > `SPA experience` without heavy JS frameworks. Dynamic content loading, seamless form handling, and component updates without page reloads.
- **💎 Glassmorphism Design UI**
  > Modern "airy" interface featuring frosted glass effects, fully responsive layout, and built-in `preloaders` for enhanced UX.
- **🧹 Automatic DB Hygiene (APScheduler)**
  > Integrated background task scheduler that automatically prunes expired tokens and deletes unverified accounts 
  > to keep the database clean.
- **🛠️ Professional Admin Panel (SQLAdmin)**
  > Comprehensive data management interface: CRUD operations, advanced search, and filtering. 
  > Pre-configured beautiful formatting for dates and user statuses.
- **🛡️ Traffic Control & Protection (Slowapi)**
  > Built-in `Rate Limiting` on critical endpoints to protect against brute-force and spam. 
  > Flexible `CORS` configuration for enhanced security.
- **🏗️ Modern Architecture (Clean Architecture)**  
  > Clean separation into layers: API, Services, Repositories, and Models.  
  > Easy maintainability and scalability via dependency inversion.
- **🚀 High Performance (uv + orjson)**  
  > Instant environment setup using the `uv` package manager.  
  > Ultra-fast data serialization via `orjson`.
- **🗄️ Data Handling (SQLAlchemy 2.0)**  
  > Fully asynchronous interaction with `PostgreSQL (asyncpg)`.  
  > Universal base repository to minimize boilerplate code.
- **🔄 Automated Migrations (Alembic)**  
  > Schema management with async support.  
  > Automatic migration application on container startup.
- **📧 Async Notifications (aiosmtplib)**  
  > Send system and transactional emails (registration confirmation, password reset) without blocking the main thread.
- **🧩 Caching (Redis + fastapi-cache2)**  
  > Integration with `Redis` to cache heavy queries, reducing DB load and improving API response time.
- **📦 Containerization & DevOps (Docker)**  
  > Ready-to-use infrastructure: app, DB, Redis, and PGAdmin — all launched with one command.  
  > Hot Reload support for fast development inside containers.
- **🧪 Reliable Testing (Pytest)**  
  > Preconfigured async API testing with `HTTPX`.  
  > Fake data generation via `Faker`, coverage reports via `pytest-cov`.
- **📘 Auto-Documentation (Swagger)**  
  > Always up-to-date interactive API docs via OpenAPI, available at `/docs`.

## 📂 Project Structure

```bash
FastH-Core-Stack/
├── app/                         # Main application package
│   ├── actions/                 # CLI scripts (e.g., create superuser)
│   ├── admin/                   # SQLAdmin configuration
│   ├── alembic/                 # Database migration history
│   ├── api/                     # API layer
│   │   ├── api_v1/              # Version 1 REST API endpoints
│   │   ├── dependencies/        # FastAPI Depends injections
│   │   ├── webhooks/            # External webhook handlers
│   │   └── __init__.py          # Router aggregation
│   ├── core/                    # Core components
│   │   ├── auth/                # FastAPI-Users security config
│   │   ├── cache/               # Redis caching setup
│   │   ├── gunicorn/            # Production WSGI config
│   │   ├── config.py            # Settings validation (pydantic-settings)
│   │   ├── db_helper.py         # SQLAlchemy engine/session setup
│   │   ├── limiter.py           # Rate limiting config
│   │   └── templates.py         # Jinja2Templates integration
│   ├── exceptions/              # Exception handling
│   │   ├── custom.py            # Custom error classes
│   │   └── handlers.py          # Global exception handlers
│   ├── middleware/              # Custom middleware
│   ├── models/                  # ORM models (SQLAlchemy)
│   ├── repositories/            # Data Access Layer
│   │   └── crud_manager.py      # Universal CRUD manager
│   ├── schemas/                 # Pydantic DTOs for validation
│   ├── services/                # Business logic layer
│   │   └── mailing/             # Email service (notifications, confirmations)
│   ├── static/                  # Static files (CSS, JS, images)
│   ├── templates/               # HTML templates with HTMX and Jinja2
│   ├── utils/                   # Utility functions
│   │   └── case_converter.py    # Table name converter
│   ├── views/                   # Routers for rendering HTML-pages and HTMX-forms
│   ├── .env                     # Environment variables (not in git)
│   ├── .env.template            # Template for .env
│   ├── alembic.ini              # Alembic config
│   ├── create_fastapi_app.py    # FastAPI app factory
│   ├── main.py                  # Dev mode entry point
│   ├── run.py                   # Gunicorn runner (for Docker)
│   └── run_main.py              # Gunicorn app launcher
├── docker-build/                # Build infrastructure
│   └── app/
│       ├── Dockerfile           # Docker build instructions
│       └── prestart.sh          # DB prep script (migrations + admin creation)
├── tests/                       # Automated tests (Pytest)
├── docker-compose.yml           # Container orchestration
├── pyproject.toml               # Project config and dependencies
└── uv.lock                      # Fixed dependency versions
```

## ⚙️ Installation and Setup

1. **Clone the repository**
> In terminal:
> ```bash
> git clone https://github.com/Mishchenko-Vladimir/FastH-Core-Stack.git
> ```
> Navigate to project directory:
> ```bash
> cd FastH-Core-Stack
> ```
 
2. **Configure environment variables**
> Fill in `.env.template` and `docker-compose.yml` with your values.

3. **Development and customization**
> Sync virtual environment:
> ```bash
> uv sync
> ```
> Apply migrations:
> ```bash
> cd app
> alembic upgrade head
> cd ..
> ```
>  Edit or add new files in `app/` — changes will be reflected automatically in the running container.
>
> Local launch (without Docker):
> ```bash
> uv run python app/main.py
> ```

4. **Run via Docker**
> If you are running the image on Windows, make sure that the files `docker-build/app/prestart.sh` and `app/run.py` use LF line endings, not CRLF.
> 
> Build image named `app`:
> ```bash
> docker compose build app
> ```
> Start containers:
> ```bash
> docker compose up -d
> ```
> Other Docker commands:
> - `docker compose ps` — view running containers
> - `docker compose logs -f app` — view app logs
> - `docker compose stop` — stop app
> - `docker compose down` — remove containers

> The app will be available at http://localhost:8000, documentation at http://localhost:8000/docs

## 📬 Contacts

### 💻 Author: Vladimir Mishchenko
- **GitHub:** [Mishchenko-Vladimir](https://github.com/Mishchenko-Vladimir)
- **Mail.ru:** [mishchienko.2001@mail.ru](mailto:mishchienko.2001@mail.ru)
- **Gmail:** [mishchieko.2001@gmail.com](mailto:mishchieko.2001@gmail.com)
- **Telegram:** [@VM_Dev](https://t.me/VM_Dev)

💌 Don’t forget to leave a ⭐ star on GitHub if you like the project! 😉

---
[↑ Back to top](#-fastapi-boilerplate)
