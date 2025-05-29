from sqlalchemy import Column, String, text, TIMESTAMP

from webserver.adapters.postgresql import BasePG


class IPAddress(BasePG):
    __tablename__ = "users"
    id = Column(String, primary_key=True, index=True)
    username = Column(String, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
