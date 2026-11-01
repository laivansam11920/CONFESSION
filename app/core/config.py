from pydantic import Field, computed_field
from pydantic_settings import BaseSettings, SettingsConfigDict

__all__ = ["Config"]


class Configs(BaseSettings):
    MONGO_URI: str = Field(..., alias="mongo_uri")
    NAME_DATABASE_MONGO: str = Field(..., alias="NAME_DATABASE")

    model_config = SettingsConfigDict(populate_by_name=True)


Config = Configs()
