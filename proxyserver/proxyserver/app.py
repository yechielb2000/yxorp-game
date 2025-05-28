from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI

from middlewares.rate_limit import RateLimitMiddleware
from proxyserver.adapters.redis import redis_instance
from settings import settings


@asynccontextmanager
async def lifespan(application: FastAPI):
    yield
    await redis_instance.close()


app = FastAPI(lifespan=lifespan)

app.add_middleware(RateLimitMiddleware, redis_client=redis_instance)

if __name__ == '__main__':
    uvicorn.run("app:app", host="0.0.0.0", port=settings.webserver_port)  # TODO: should be as webserver port.
