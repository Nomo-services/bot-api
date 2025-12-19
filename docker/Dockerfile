FROM python:3.13-slim

ENV PYTHONUNBUFFERED=1 \
    POETRY_VIRTUALENVS_CREATE=false \
    PIP_NO_CACHE_DIR=1

WORKDIR /app

RUN apt-get update \
 && apt-get install -y --no-install-recommends \
      build-essential libpq-dev curl\
 && rm -rf /var/lib/apt/lists/*

RUN pip install --upgrade pip \
 && pip install poetry

COPY pyproject.toml poetry.lock README.md ./

RUN poetry install --no-interaction --no-ansi --no-root

COPY src/           src/
COPY migrations/    migrations/
COPY alembic.ini    ./
COPY data/          data/
COPY ./bin/         /app/bin/

RUN chmod +x /app/bin/run_app.sh