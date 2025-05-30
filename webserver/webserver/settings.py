from pydantic import Field
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    postgresql_db: str = Field(..., alias="POSTGRESQL_DB")
    postgresql_user: str = Field(..., alias="POSTGRESQL_USER")
    postgresql_password: str = Field(..., alias="POSTGRESQL_PASSWORD")
    postgresql_host: str = Field(..., alias="POSTGRESQL_HOST")
    postgresql_port: int = Field(..., alias="POSTGRESQL_PORT")

    infra_logs_path: str = Field(..., alias="WEBSERVER_INFRA_LOGS")
    user_actions_logs_path: str = Field(..., alias="WEBSERVER_USER_ACTIONS_LOGS")
    jwt_secret_key: str = Field(..., alias="WEBSERVER_JWT_KEY")

    class Config:
        env_file = "../../.env"
        extra = "ignore"

    @property
    def elasticsearch_url(self) -> str:
        return f"http://{self.elasticsearch_host}:{self.elasticsearch_port}"

    @property
    def postgresql_url(self) -> str:
        return (
            f"postgresql+asyncpg://{self.postgresql_user}:{self.postgresql_password}"
            f"@{self.postgresql_host}:{self.postgresql_port}/{self.postgresql_db}"
        )


settings = Settings()
