FROM python:3.14-slim-bookworm

ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

COPY --from=ghcr.io/astral-sh/uv:0.9.18 /uv /uvx /bin/

WORKDIR /app

COPY pyproject.toml uv.lock ./

RUN uv sync --locked --no-install-project --no-dev
ENV PATH="/app/.venv/bin:$PATH"

COPY docker-build/app/prestart.sh ./prestart.sh

COPY app ./

RUN chmod +x prestart.sh
RUN chmod +x run.py

ENTRYPOINT ["./prestart.sh"]
CMD ["./run.py"]