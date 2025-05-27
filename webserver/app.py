from contextlib import asynccontextmanager

import uvicorn
from dotenv import load_dotenv
from fastapi import FastAPI

from webserver.adapters.postgresql import pg_engine, BasePG
from webserver.logger_setup import setup_logger


@asynccontextmanager
async def lifespan(a: FastAPI):
    load_dotenv()
    setup_logger()
    async with pg_engine.begin() as conn:
        await conn.run_sync(BasePG.metadata.create_all)
    yield


app = FastAPI(lifespan=lifespan)

if __name__ == '__main__':
    uvicorn.run("cnc:app", host="0.0.0.0", port=8000)
