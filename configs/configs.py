from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field, computed_field
from datetime import datetime
from flask_babel import gettext as _

from app.utils.fb_page_id import get_facebook_page_info as get_id


class Settings(BaseSettings):

    MONGO_URI: str = Field(..., alias="MONGO_URI")
    MONGO_MAIN_DB: str = Field(default="Confession", alias="MONGO_MAIN_DB")

    GOOGLE_AI_API_KEY: str = Field(..., alias="GOOGLE_AI_API_KEY")
    MODEL_GOOGLE_AI: str = Field(default="gemma-4-31b-it", alias="MODEL_GOOGLE_AI")

    CHECK_SAME_DOCS: bool = Field(default=True, alias="CHECK_SAME_DOCS")
    TIME_OUT_CONFESSION: int = Field(default=86400, alias="TIME_OUT_CONFESSION")
    SIMILARITY_THRESHOLD: float = Field(default=64, alias="SIMILARITY_THRESHOLD")

    HOST: str = Field(default="0.0.0.0", alias="HOST")
    PORT: int = Field(default=2011, alias="PORT")
    DEBUG: bool = Field(default=False, alias="DEBUG")
    TEST: bool = Field(default=False, alias="TEST")
    SECRET_KEY: str = Field(..., alias="SECRET_KEY")

    CHANGE_GET_DATA_BY_WEB: bool = Field(default=True, alias="CHANGE_GET_DATA_BY_WEB")
    CHANGE_GET_DATA_BY_GOOGLE_FORM: bool = Field(
        default=False, alias="CHANGE_GET_DATA_BY_GOOGLE_FORM"
    )
    GET_EMAIL: bool = Field(default=False, alias="GET_EMAIL")
    NAME_GROUP_USE_PROJECT: str = Field(default="", alias="NAME_GROUP_USE_PROJECT")
    MODERATION_CONFESSION: bool = Field(default=False, alias="MODERATION_CONFESSION")
    MAX_LEN_CONFESSION_ALLOW: int = Field(
        default=1000, alias="MAX_LEN_CONFESSION_ALLOW"
    )
    MAX_LEN_CONFESSION_VIP_ALLOW: int = Field(
        default=10 * 10 ^ 3, alias="MAX_LEN_CONFESSION_VIP_ALLOW"
    )
    MIN_LEN_CONFESSION_ALLOW: int = Field(default=1, alias="MIN_LEN_CONFESSION_ALLOW")
    MIN_LEN_CONFESSION_VIP_ALLOW: int = Field(
        default=0, alias="MIN_LEN_CONFESSION_VIP_ALLOW"
    )
    TRACKING_USER: bool = Field(default=False, alias="TRACKING_USER")
    TOPIC_COLOR: str = Field(default="#000000", alias="TOPIC_COLOR")
    MAX_MODERATION_SCORE: float = Field(default=55, alias="MAX_MODERATION_SCORE")
    MAX_DOCS_GET: int = Field(default=100, alias="MAX_DOCS_GET")
    TOPIC_SENTENCE: str = Field(
        default=f"{_("Tổng hợp Confession ngày")} {datetime.now().strftime("%d/%m/%Y")}\n",
        alias="TOPIC_SENTENCE",
    )
    ALWAYS_ON: bool = Field(default=True, alias="ALWAYS_ON")
    VIP_CFS_ON: bool = Field(default=True, alias="VIP_CFS_ON")

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

    @computed_field
    @property
    def MAX_CONTENT_LENGTH(self) -> int:
        return (self.MAX_LEN_CONFESSION_ALLOW * 9) + 2048

    FACEBOOK_PAGE_ACCESS_TOKEN: str = Field(..., alias="FACEBOOK_PAGE_ACCESS_TOKEN")

    @computed_field
    @property
    def FACEBOOK_PAGE_ID(self) -> str:
        return get_id(self.FACEBOOK_PAGE_ACCESS_TOKEN)

    RENDER_EXTERNAL_URL: str = Field(default="", alias="RENDER_EXTERNAL_URL")

    HOUR: int = Field(default=11, alias="HOUR")
    MINUTE: int = Field(default=30, alias="MINUTE")

    REDIS_URL: str = Field(default="", alias="REDIS_URL") #NOT USE

    model_config = SettingsConfigDict(populate_by_name=True)


Config = Settings()
