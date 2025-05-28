from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI

from middlewares.rate_limit import RateLimitMiddleware
from middlewares.reverse_proxy import ProxyMiddleware
from middlewares.slowloris import SlowlorisMiddleware
from proxyserver.adapters.redis import redis_instance
from settings import settings


@asynccontextmanager
async def lifespan(application: FastAPI):
    yield
    await redis_instance.close()


app = FastAPI(lifespan=lifespan)

app.add_middleware(ProxyMiddleware)
app.add_middleware(RateLimitMiddleware, redis_client=redis_instance)
app.add_middleware(SlowlorisMiddleware)

if __name__ == '__main__':
    port = settings.webserver_port + 1
    uvicorn.run("app:app", host="0.0.0.0", port=port)
