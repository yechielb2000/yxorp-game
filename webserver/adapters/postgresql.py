import os

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker


_USER = os.environ.get("POSTGRESQL_USER")
_PASSWORD = os.environ.get("POSTGRESQL_PASSWORD")
_DATABASE = os.environ.get("POSTGRESQL_DATABASE")
_HOST = os.environ.get("POSTGRESQL_HOST")
_PORT = os.environ.get("POSTGRESQL_PORT")

DATABASE_URL = f"postgresql+asyncpg://{_USER}:{_PASSWORD}@{_HOST}:{_PORT}/{_DATABASE}"

engine = create_async_engine(DATABASE_URL, echo=True)

AsyncSessionLocal = async_sessionmaker(bind=engine, expire_on_commit=False, class_=AsyncSession)


async def get_postgresql_db():
    async with AsyncSessionLocal() as session:
        yield session
