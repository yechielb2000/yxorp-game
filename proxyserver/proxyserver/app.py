from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI
from redis.asyncio import Redis

from proxyserver.adapters.redis import get_redis
from settings import settings

app = FastAPI()
app.state.redis.redis_client: Redis


@asynccontextmanager
async def lifespan(a: FastAPI):
    a.state.redis_client = get_redis()
    yield
    await a.state.redis_client.close()


if __name__ == '__main__':
    uvicorn.run("app:app", host="0.0.0.0", port=settings.webserver_port)  # TODO: should be as webserver port.
