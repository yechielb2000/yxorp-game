from contextlib import asynccontextmanager

import uvicorn
from dotenv import load_dotenv
from fastapi import FastAPI
from sqlalchemy.ext.asyncio import AsyncConnection

from webserver.adapters.postgresql import pg_engine, BasePG
from webserver.routers import countries_router, user_router, ips_router
from webserver.utils.logger_setup import setup_logger


@asynccontextmanager
async def lifespan(a: FastAPI):
    load_dotenv()
    setup_logger()
    conn: AsyncConnection
    async with pg_engine.begin() as conn:
        await conn.run_sync(BasePG.metadata.create_all)
    yield


app = FastAPI(lifespan=lifespan)
app.include_router(countries_router)
app.include_router(ips_router)
app.include_router(user_router)

if __name__ == '__main__':
    uvicorn.run("app:app", host="0.0.0.0", port=8000)
