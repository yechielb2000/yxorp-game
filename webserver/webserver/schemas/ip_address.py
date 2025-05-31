from datetime import datetime

from pydantic import BaseModel, IPvAnyAddress


class IPAddressBase(BaseModel):
    address: IPvAnyAddress
    searched_at: datetime
    country: str


class IPAddressCreate(IPAddressBase):
    pass


class IPAddressUpdate(BaseModel):
    address: IPvAnyAddress | str
    searched_at: datetime | None = None
    country: str | None = None


class IPAddressRead(IPAddressBase):
    class Config:
        from_attributes = True
