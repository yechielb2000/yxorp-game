from contextlib import asynccontextmanager

from fastapi import FastAPI
from settings import settings
import uvicorn
from proxyserver.adapters.redis import get_redis
app = FastAPI()


@asynccontextmanager
async def lifespan(a: FastAPI):
    redis_client = get_redis()

    yield

if __name__ == '__main__':
    uvicorn.run("app:app", host="0.0.0.0", port=settings.webserver_port) # TODO: should be as webserver port.