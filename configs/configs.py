from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field


class Settings(BaseSettings):

    MONGO_URI: str = Field(..., alias="MONGO_URI")
    MONGO_MAIN_DB: str = Field(default="Confession", alias="MONGO_MAIN_DB")

    GOOGLE_AI_API_KEY: str = Field(..., alias="GOOGLE_AI_API_KEY")

    CHECK_SAME_DOCS: bool = Field(True, alias="CHECK_SAME_DOCS")
    TIME_OUT_CONFESSION: int = Field(86400, alias="TIME_CONFESSION_MAX")
    SIMILARITY_THRESHOLD: float = Field(default=0.64, alias="SIMILARITY_THRESHOLD")

    HOST: str = Field(default="0.0.0.0", alias="HOST")
    PORT: int = Field(default=2011, alias="PORT")
    DEBUG: bool = Field(False, alias="DEBUG")
    SECRET_KEY: str = Field(..., alias="SECRET_KEY")

    CHANGE_GET_DATA_BY_WEB: bool = Field(True, alias="CHANGE_GET_DATA_BY_WEB")
    GET_EMAIL: bool = Field(False, alias="GET_EMAIL")
    NAME_GROUP_USE_PROJECT: str = Field(default="", alias="NAME_GROUP_USE_PROJECT")

    BABEL_DEFAULT_LOCALE: str = Field(default="en", alias="BABEL_DEFAULT_LOCALE")
    BABEL_TRANSLATION_DIRECTORIES: str = Field(default="translations", alias="BABEL_TRANSLATION_DIRECTORIES")

    model_config = SettingsConfigDict(populate_by_name=True)


Config = Settings()
