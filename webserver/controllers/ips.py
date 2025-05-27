from datetime import datetime
from typing import Optional, List

from fastapi import Depends
from sqlalchemy import select, delete, func, and_, update
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.orm import Session

from webserver.adapters.postgresql import get_postgresql_db
from webserver.models.ip_address import IPAddress
from webserver.schemas.ip_address import IPAddressCreate, IPAddressUpdate


class IpsController:
    def __init__(self, postgres: Session):
        self.postgres = postgres

    def get_ip_info(self, address: str) -> Optional[IPAddress]:
        stmt = select(IPAddress).where(IPAddress.address == address)
        address_info = self.postgres.execute(stmt).one_or_none()
        return address_info

    def create_ip_info(self, ip_info: IPAddressCreate) -> None:
        stmt = insert(IPAddress).values(ip_info.model_dump())

        stmt = stmt.on_conflict_do_update(
            index_elements=[IPAddress.address],
            set_={"searched_at": func.now()}
        )

        self.postgres.execute(stmt)
        self.postgres.commit()

    def delete_ip_info(self, address: str) -> None:
        stmt = delete(IPAddress).where(IPAddress.address == address)
        self.postgres.execute(stmt)
        self.postgres.commit()

    def update_ip_info(self, ip_info: IPAddressUpdate) -> None:
        address = ip_info.address
        update_values = ip_info.model_dump(exclude_none=True, exclude={"address"})
        stmt = update(IPAddress).where(IPAddress.address == address).values(**update_values)
        self.postgres.execute(stmt)
        self.postgres.commit()

    def get_top_queried_countries(self, top: int = 5) -> List[IPAddress]:
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
            end_time: Optional[datetime]) -> List[IPAddress]:
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
