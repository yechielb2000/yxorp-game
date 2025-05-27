import os

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import declarative_base

USER = os.environ.get("POSTGRESQL_USER")
PASSWORD = os.environ.get("POSTGRESQL_PASSWORD")
DATABASE = os.environ.get("POSTGRESQL_DB")
HOST = os.environ.get("POSTGRESQL_HOST")
PORT = os.environ.get("POSTGRESQL_PORT")

DATABASE_URL = f"postgresql+asyncpg://{USER}:{PASSWORD}@{HOST}:{PORT}/{DATABASE}"

BasePG = declarative_base()
pg_engine = create_async_engine(DATABASE_URL, echo=True)

AsyncSessionLocal = async_sessionmaker(bind=pg_engine, expire_on_commit=False, class_=AsyncSession)


async def get_postgresql_db():
    async with AsyncSessionLocal() as session:
        yield session
