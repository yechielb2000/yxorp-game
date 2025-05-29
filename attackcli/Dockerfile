FROM ghcr.io/astral-sh/uv:python3.13-alpine

WORKDIR /attackcli

ENV UV_COMPILE_BYTECODE=1

COPY pyproject.toml .
COPY uv.lock .

ENV UV_PROJECT_ENVIRONMENT="/usr/local"

RUN uv sync --frozen --no-cache

COPY . .

COPY attack /usr/local/bin/attack
RUN chmod +x /usr/local/bin/attack

ENTRYPOINT ["sh"]


