from base import GetData
from app.schema.confession import ConfessionSchema
from app.services.save_data import SaveConfession
from app.utils.return_home import home
from configs import Config

from flask import request, flash, Response
from flask_babel import _

import uuid
import time

__all__ = ["get_data_web"]


class GetDataWeb(GetData):

    def get_data(self) -> Response:

        confession: str = request.form.get("confession", "")
        email: str = request.form.get("email", "anonymous")

        if not confession:
            flash("Đã xãy ra 1 lỗi nào đó khiến conffession của bạn không tồn tại")
            return home()

        data = ConfessionSchema(
            confession=confession,
            email=email,
            confession_id=str(uuid.uuid4()),
            post_time=int(time.time()),
        )

        res = SaveConfession.save_to_db(data)

        flash(res.get("msg", _("Đã xảy ra 1 lỗi nào đó")), res.get("status", "error"))
        return home()


if Config.CHANGE_GET_DATA_BY_WEB:
    get_data_web: GetDataWeb = GetDataWeb()
else:
    get_data_web: None = None
