from pydantic import Field
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    redis_password: str = Field(..., alias="REDIS_PASSWORD")

    postgres_user: str = Field(..., alias="POSTGRES_USER")
    postgres_password: str = Field(..., alias="POSTGRES_PASSWORD")

    postgresql_db: str = Field(..., alias="POSTGRESQL_DB")
    postgresql_user: str = Field(..., alias="POSTGRESQL_USER")
    postgresql_password: str = Field(..., alias="POSTGRESQL_PASSWORD")
    postgresql_host: str = Field(..., alias="POSTGRESQL_HOST")
    postgresql_port: int = Field(..., alias="POSTGRESQL_PORT")

    elasticsearch_host: str = Field(..., alias="ELASTICSEARCH_HOST")
    elasticsearch_port: int = Field(..., alias="ELASTICSEARCH_PORT")

    class Config:
        env_file = ".env"
        extra = "ignore"

    @property
    def elasticsearch_url(self) -> str:
        return f"https://{self.elasticsearch_host}:{self.elasticsearch_port}"

    @property
    def postgresql_url(self) -> str:
        return (
            f"postgresql+asyncpg://{self.postgresql_user}:{self.postgresql_password}"
            f"@{self.postgresql_host}:{self.postgresql_port}/{self.postgresql_db}"
        )


settings = Settings()
