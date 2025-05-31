from datetime import datetime
from typing import Optional, List

from fastapi import Depends
from sqlalchemy import select, delete, func, and_, update
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.ext.asyncio import AsyncSession

from webserver.adapters.postgresql import get_postgresql_db
from webserver.models.ip_address import IPAddress
from webserver.schemas.ip_address import IPAddressCreate, IPAddressUpdate, IPAddressRead
from webserver.utils.logger_setup import get_infra_logger


class IpsController:
    def __init__(self, postgres: AsyncSession):
        self.postgres = postgres
        self.infra_logger = get_infra_logger()

    async def get_ip_info(self, address: str) -> IPAddressRead | None:
        self.infra_logger.info("Get ip info", extra={"address": address})
        stmt = select(IPAddress).where(IPAddress.address == address)
        result = await self.postgres.execute(stmt)
        row = result.scalar_one_or_none()
        if row:
            return IPAddressRead.model_validate(row)
        return None

    async def create_ip_info(self, ip_info: IPAddressCreate) -> None:
        self.infra_logger.info("Create ip info", extra={"ip_info": ip_info.model_dump()})
        stmt = insert(IPAddress).values(ip_info.model_dump())
        await self.postgres.execute(stmt)
        await self.postgres.commit()

    async def upsert_ip_info(self, ip: str, country: str) -> IPAddressRead:
        self.infra_logger.info("Upsert ip info", extra={"ip": ip, "country": country})
        stmt = insert(IPAddress).values(address=ip, country=country)
        stmt = stmt.on_conflict_do_update(
            index_elements=[IPAddress.address],
            set_={"country": country, "searched_at": func.now()}
        ).returning(IPAddress.address, IPAddress.country, IPAddress.searched_at)

        result = await self.postgres.execute(stmt)
        await self.postgres.commit()
        row = result.first()
        return IPAddressRead(address=row.address, country=row.country, searched_at=row.searched_at)

    async def delete_ip_info(self, address: str) -> None:
        self.infra_logger.info("Delete ip info", extra={"address": address})
        stmt = delete(IPAddress).where(IPAddress.address == address)
        await self.postgres.execute(stmt)
        await self.postgres.commit()

    async def update_ip_info(self, ip_info: IPAddressUpdate) -> None:
        self.infra_logger.info("Update ip info", extra={"ip_info": ip_info.model_dump()})
        address = ip_info.address
        update_values = ip_info.model_dump(exclude_none=True, exclude={"address"})
        stmt = update(IPAddress).where(IPAddress.address == address).values(**update_values)
        await self.postgres.execute(stmt)
        await self.postgres.commit()

    async def get_top_queried_countries(self, top: int = 5) -> List[str]:
        self.infra_logger.info("Get top queried countries", extra={"top": top})
        stmt = (
            select(IPAddress.country)
            .group_by(IPAddress.country)
            .order_by(func.count(IPAddress.address).desc())
            .limit(top)
        )
        result = await self.postgres.execute(stmt)
        countries = result.scalars().all()
        return countries

    async def get_ips_by_country(
            self,
            country: str,
            start_time: datetime | None = None,
            end_time: datetime | None = None) -> List[str]:
        self.infra_logger.info("Get ips by country",
                               extra={"country": country, "start_time": start_time, "end_time": end_time})
        stmt = select(IPAddress.address).where(IPAddress.country == country)

        if start_time and end_time:
            stmt = stmt.where(and_(IPAddress.searched_at >= start_time, IPAddress.searched_at <= end_time))
        elif start_time:
            stmt = stmt.where(IPAddress.searched_at >= start_time)
        elif end_time:
            stmt = stmt.where(IPAddress.searched_at <= end_time)

        result = await self.postgres.execute(stmt)
        ips = result.scalars().all()
        return ips


def get_ips_controller(postgres=Depends(get_postgresql_db)):
    return IpsController(postgres)
