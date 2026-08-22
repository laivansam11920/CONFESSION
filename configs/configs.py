from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field


class Settings(BaseSettings):

    # DATABASE CONFIGS
    MONGO_URI: str = Field(..., alias="MONGO_URI")
    MONGO_MAIN_DB: str = Field(default="Confession", alias="MONGO_MAIN_DB")
    CHECK_SAME_DOCS: bool = Field(True, alias="CHECK_SAME_DOCS")
    TIME_OUT_CONFESSION: int = Field(86400, alias="TIME_CONFESSION_MAX")

    SIMILARITY_THRESHOLD: float = Field(default=0.64, alias="SIMILARITY_THRESHOLD")

    model_config = SettingsConfigDict(populate_by_name=True)


Config = Settings()
