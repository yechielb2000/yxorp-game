from datetime import datetime
from typing import Optional, List

from fastapi import Depends
from sqlalchemy import select, delete, func, and_, update
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.ext.asyncio import AsyncSession

from webserver.adapters.postgresql import get_postgresql_db
from webserver.models.ip_address import IPAddress
from webserver.schemas.ip_address import IPAddressCreate, IPAddressUpdate, IPAddressRead


class IpsController:
    def __init__(self, postgres: AsyncSession):
        self.postgres = postgres

    async def get_ip_info(self, address: str) -> Optional[IPAddressRead]:
        stmt = select(IPAddress).where(IPAddress.address == address)
        result = await self.postgres.execute(stmt)
        row = result.scalar_one_or_none()
        if row:
            return IPAddressRead.model_validate(row)
        return None

    async def create_ip_info(self, ip_info: IPAddressCreate) -> None:
        stmt = insert(IPAddress).values(ip_info.model_dump())
        await self.postgres.execute(stmt)
        await self.postgres.commit()

    async def upsert_ip_info(self, ip: str, country: str) -> IPAddressRead:
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
        stmt = delete(IPAddress).where(IPAddress.address == address)
        await self.postgres.execute(stmt)
        await self.postgres.commit()

    async def update_ip_info(self, ip_info: IPAddressUpdate) -> None:
        address = ip_info.address
        update_values = ip_info.model_dump(exclude_none=True, exclude={"address"})
        stmt = update(IPAddress).where(IPAddress.address == address).values(**update_values)
        await self.postgres.execute(stmt)
        await self.postgres.commit()

    def get_top_queried_countries(self, top: int = 5) -> List[IPAddressRead]:
        stmt = (
            select(IPAddress.country)
            .group_by(IPAddress.country)
            .order_by(func.count(IPAddress.address).desc())
            .limit(top)
        )
        top_x_countries = self.postgres.execute(stmt).scalars().all()
        return top_x_countries

    def get_ips_by_country(
            self,
            country: str,
            start_time: Optional[datetime],
            end_time: Optional[datetime]) -> List[IPAddressRead]:
        stmt = select(IPAddress.address).where(IPAddress.country == country)

        if start_time and end_time:
            stmt = stmt.where(and_(IPAddress.searched_at >= start_time, IPAddress.searched_at <= end_time))
        elif start_time:
            stmt = stmt.where(IPAddress.searched_at >= start_time)
        elif end_time:
            stmt = stmt.where(IPAddress.searched_at <= end_time)

        ips = self.postgres.execute(stmt).scalars().all()
        return ips


def get_ips_controller(postgres=Depends(get_postgresql_db)):
    return IpsController(postgres)
