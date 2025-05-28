from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI

from middlewares.rate_limit import RateLimitMiddleware
from proxyserver.adapters.redis import get_redis
from settings import settings


@asynccontextmanager
async def lifespan(application: FastAPI):
    redis_client = get_redis()

    app.add_middleware(RateLimitMiddleware, redis_client=redis_client)
    yield
    await redis_client.close()


app = FastAPI(lifespan=lifespan)


if __name__ == '__main__':
    uvicorn.run("app:app", host="0.0.0.0", port=settings.webserver_port)  # TODO: should be as webserver port.
