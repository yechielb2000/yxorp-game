FROM python:3.13-alpine

COPY --from=ghcr.io/astral-sh/uv:latest /uv /bin/uv

WORKDIR /app

ENV UV_COMPILE_BYTECODE=1

COPY ../pyproject.toml .
COPY ../uv.lock .
COPY . .

#RUN uv sync --frozen --no-cache

RUN uv pip install --system elasticsearch fastapi loguru python-dotenv sqlalchemy uvicorn asyncpg ipwhois

#ENV PATH="/app/.venv/bin:$PATH"

ENV PYTHONPATH=/app

CMD ["uvicorn", "webserver.app:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]



