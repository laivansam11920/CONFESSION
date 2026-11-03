from pydantic import Field, computed_field
from pydantic_settings import BaseSettings, SettingsConfigDict
from dotenv import load_dotenv, find_dotenv

__all__ = ["Config"]

load_dotenv(find_dotenv(), override=True)


class Configs(BaseSettings):
    MONGO_URI: str = Field(..., alias="MONGO_URI")
    NAME_DATABASE_MONGO: str = Field(default="Confession", alias="NAME_DATABASE")

    model_config = SettingsConfigDict(populate_by_name=True)


Config = Configs()
