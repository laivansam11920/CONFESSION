from base import GetData
from app.schema.confession import ConfessionSchema
from app.services.save_data import SaveConfession
from configs import Config

from flask import request, flash, redirect, url_for
from flask_babel import Babel, gettext as _ #type: ignore

import uuid
import time

__all__ = ["get_data_web"]


class GetDataWeb(GetData):

    def get_data(self):

        confession: str = request.form.get("confession", "")
        email: str = request.form.get("email", "anonymous")

        data = ConfessionSchema(
            confession=confession,
            email=email,
            confession_id=str(uuid.uuid4()),
            post_time=int(time.time()),
        )

        res = SaveConfession.save_to_db(data)

        flash(res.get("msg", _("Đã xảy ra 1 lỗi nào đó")), res.get("status", "error"))
        return redirect(
            url_for(
                "main_route.index",
                lang=request.args.get(
                    "lang", request.accept_languages.best_match(["vi", "en"])
                ),
            )
        )

if Config.CHANGE_GET_DATA_BY_WEB:
    get_data_web: GetDataWeb = GetDataWeb()
else:
    get_data_web: None = None
