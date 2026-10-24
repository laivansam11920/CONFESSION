from flask import Blueprint, request

from app.extensions.limiter import limiter
from app.extensions.crfs import crfs
from configs import Config

__all__ = ["get_data"]

get_data: Blueprint = Blueprint("get_data", __name__)


if Config.CHANGE_GET_DATA_BY_WEB:

    @get_data.post("/submit-confession")
    def get_confession():
        from app.controller.get_data import get_data_main

        return get_data_main.get_data(get_data_by_web=True)


if Config.CHANGE_GET_DATA_BY_GOOGLE_FORM:

    @get_data.post("/submit-confession-form")
    @crfs.exempt
    @limiter.limit(
        Config.DEFAULT_RATE_LIMIT,
        exempt_when=lambda: request.headers.get("X-App-Secret") == Config.SECRET_KEY,
    )
    def get_confession_form():
        from app.controller.get_data import get_data_main

        return get_data_main.get_data(get_data_by_web=False)
