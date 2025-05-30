from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from webserver.adapters.postgresql import get_postgresql_db
from webserver.models.user import User
from webserver.schemas.user import UserCreate
from webserver.utils.logger_setup import get_infra_logger
from webserver.utils.passwords import hash_password


class UserController:
    def __init__(self, postgres: AsyncSession):
        self.postgres = postgres
        self.infra_logger = get_infra_logger()

    async def get_user_by_username(self, username: str) -> User | None:
        self.infra_logger.info("Get user by username", extra={"username": username})
        stmt = select(User).where(User.username == username)
        result = await self.postgres.execute(stmt)
        return result.scalar_one_or_none()

    async def get_user_by_id(self, user_id: int) -> User | None:
        self.infra_logger.info("Get user by id", extra={"user_id": user_id})
        stmt = select(User).where(User.id == user_id)
        result = await self.postgres.execute(stmt)
        return result.scalar_one_or_none()

    async def create_user(self, user: UserCreate) -> User:
        self.infra_logger.info("Create user", extra={"username": user.username})
        hashed_pw = hash_password(user.password)
        db_user = User(username=user.username, hashed_password=hashed_pw)
        self.postgres.add(db_user)
        await self.postgres.commit()
        await self.postgres.refresh(db_user)
        return db_user


def get_user_controller(postgres=Depends(get_postgresql_db)) -> UserController:
    return UserController(postgres)
