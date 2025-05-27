from sqlalchemy import Column, String, text, TIMESTAMP

from webserver.adapters.postgresql import BasePG


class IPAddress(BasePG):
    __tablename__ = "ips"

    address = Column(String, primary_key=True, index=True)
    searched_at = Column(TIMESTAMP, server_default=text("CURRENT_TIMESTAMP"))
    country = Column(String, index=True)
