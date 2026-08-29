from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field
from datetime import datetime
from flask_babel import gettext as _


class Settings(BaseSettings):

    MONGO_URI: str = Field(..., alias="MONGO_URI")
    MONGO_MAIN_DB: str = Field(default="Confession", alias="MONGO_MAIN_DB")

    GOOGLE_AI_API_KEY: str = Field(..., alias="GOOGLE_AI_API_KEY")
    MODEL_GOOGLE_AI: str = Field(default="gemma-4-31b-it", alias="MODEL_GOOGLE_AI")

    CHECK_SAME_DOCS: bool = Field(True, alias="CHECK_SAME_DOCS")
    TIME_OUT_CONFESSION: int = Field(86400, alias="TIME_OUT_CONFESSION")
    SIMILARITY_THRESHOLD: float = Field(default=0.64, alias="SIMILARITY_THRESHOLD")

    HOST: str = Field(default="0.0.0.0", alias="HOST")
    PORT: int = Field(default=2011, alias="PORT")
    DEBUG: bool = Field(False, alias="DEBUG")
    TEST: bool = Field(False, alias="TEST")
    SECRET_KEY: str = Field(..., alias="SECRET_KEY")

    CHANGE_GET_DATA_BY_WEB: bool = Field(True, alias="CHANGE_GET_DATA_BY_WEB")
    GET_EMAIL: bool = Field(False, alias="GET_EMAIL")
    NAME_GROUP_USE_PROJECT: str = Field(default="", alias="NAME_GROUP_USE_PROJECT")
    MODERATION_CONFESSION: bool = Field(False, alias="MODERATION_CONFESSION")
    MAX_LEN_CONFESSION_ALLOW: int = Field(default=500, alias="MAX_LEN_CONFESSION_ALLOW")
    TRACKING_USER: bool = Field(False, alias="TRACKING_USER")
    TOPIC_COLOR: str = Field(default="#000000", alias="TOPIC_COLOR")
    MAX_MODERATION_SCORE: float = Field(default=55, alias="MAX_MODERATION_SCORE")
    TOPIC_SENTENCE: str = Field(
        default=f"{_("Tổng hợp Confession ngày")} {datetime.now().strftime("%d/%m/%Y")}\n",
        alias="TOPIC_SENTENCE",
    )

    BABEL_DEFAULT_LOCALE: str = Field(default="en", alias="BABEL_DEFAULT_LOCALE")
    BABEL_TRANSLATION_DIRECTORIES: str = Field(
        default="translations", alias="BABEL_TRANSLATION_DIRECTORIES"
    )

    MAX_THREADPOOL_EXECUTOR_WORKER: int = Field(
        default=5, alias="MAX_THREADPOOLEXECUTOR_WORKER"
    )

    SESSION_COOKIE_SECURE: bool = Field(default=True, alias="SESSION_COOKIE_SECURE")
    SESSION_COOKIE_SAMESITE: str = Field(default="Lax", alias="SESSION_COOKIE_SAMESITE")
    SESSION_COOKIE_HTTPONLY: bool = Field(default=True, alias="SESSION_COOKIE_HTTPONLY")

    FACEBOOK_PAGE_ID: str = Field(..., alias="FACEBOOK_PAGE_ID")
    FACEBOOK_PAGE_ACCESS_TOKEN: str = Field(..., alias="FACEBOOK_PAGE_ACCESS_TOKEN")

    RENDER_EXTERNAL_URL: str = Field(default="", alias="RENDER_EXTERNAL_URL")

    HOUR: int = Field(default=11, alias="HOUR")
    MINUTE: int = Field(default=30, alias="MINUTE")

    model_config = SettingsConfigDict(populate_by_name=True)


Config = Settings()
