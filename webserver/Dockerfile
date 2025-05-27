FROM python:3.13-slim

COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

COPY ../uv.lock /app
COPY ../pyproject.toml /app

COPY . /app

WORKDIR /app

RUN uv sync --frozen --no-cache
