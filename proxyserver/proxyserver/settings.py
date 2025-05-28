from pydantic import Field
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    redis_password: str = Field(..., alias="REDIS_PASSWORD")
    redis_user: str = Field(..., alias="REDIS_USER")
    redis_host: str = Field(..., alias="REDIS_HOST")
    redis_port: str = Field(..., alias="REDIS_PORT")
    webserver_url: str = Field(..., alias="WEBSERVER_URL")
    webserver_port: int = Field(..., alias="WEBSERVER_PORT")

    class Config:
        env_file = "../../.env"
        extra = "ignore"


settings = Settings()
