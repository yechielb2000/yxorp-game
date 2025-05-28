FROM ghcr.io/astral-sh/uv:python3.13-alpine

WORKDIR /attackcli

ENV UV_COMPILE_BYTECODE=1

COPY pyproject.toml .
COPY uv.lock .

ENV UV_PROJECT_ENVIRONMENT="/usr/local"

RUN uv venv && uv pip install -r requirements.txt

COPY . .

ENTRYPOINT ["sh"]


