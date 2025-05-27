from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import declarative_base

from webserver.settings import Settings

BasePG = declarative_base()
pg_engine = create_async_engine(Settings.postgresql_url, echo=True)

AsyncSessionLocal = async_sessionmaker(bind=pg_engine, expire_on_commit=False, class_=AsyncSession)


async def get_postgresql_db():
    async with AsyncSessionLocal() as session:
        yield session
