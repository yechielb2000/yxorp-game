from sqlalchemy import Column, Integer, String, text, TIMESTAMP

from webserver.adapters.postgresql import PG_Base


class IPAddress(PG_Base):
    __tablename__ = "ips"

    id = Column(Integer, primary_key=True, index=True)
    address = Column(String, unique=True, index=True)
    searched_at = Column(TIMESTAMP, server_default=text("CURRENT_TIMESTAMP"))
    country = Column(String, index=True)
