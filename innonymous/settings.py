from urllib.parse import quote_plus

from pydantic import BaseSettings, Field


class _MongoSettings(BaseSettings):
    username: str = Field(..., env="MONGO_USERNAME")
    password: str = Field(..., env="MONGO_PASSWORD")
    host: str = Field("localhost", env="MONGO_HOST")
    port: int = Field(27017, env="MONGO_PORT")

    @property
    def url(self) -> str:
        credentials = f"{quote_plus(self.username)}:{quote_plus(self.password)}"
        address = f"{self.host}:{self.port}"
        return f"mongodb://{credentials}@{address}"

    class Config:
        env_file = ".env"


class Settings:
    mongo = _MongoSettings()
