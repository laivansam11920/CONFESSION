from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field


class Config(BaseSettings):

    # DATABASE CONFIGS
    MONGO_URI: str = Field(..., alias="MONGO_URI")
    MONGO_MAIN_DB: str = Field(default="CONFESSION", alias="MONGO_MAIN_DB")
    CHECK_SAME_DOCS: bool = Field(True, alias="CHECK_SAME_DOCS")
