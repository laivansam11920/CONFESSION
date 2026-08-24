from base import GetData
from app.schema.confession import ConfessionSchema
from app.services.save_data import SaveConfession
from app.utils.return_home import home
from app.validation.check_input_data import check_input_data
from configs import Config

from flask import flash, Response
from flask_babel import Babel, gettext as _

import uuid
import time

__all__ = ["get_data_web"]


class GetDataWeb(GetData):

    @check_input_data
    def get_data(self, email="", confession="") -> Response:

        if not confession:
            flash(
                _(
                    "Rất tiếc, hệ thống chưa nhận được nội dung confession của bạn. Vui lòng kiểm tra và gửi lại nhé!"
                )
            )
            return home()

        data = ConfessionSchema(
            confession=confession,
            email=email,
            confession_id=str(uuid.uuid4()),
            post_time=int(time.time()),
        )

        res = SaveConfession.save_to_db(data)

        flash(
            res.get(
                "msg",
                _(
                    "Rất tiếc, quá trình xử lý gặp chút sự cố. Bạn vui lòng thử lại sau nhé."
                ),
            ),
            res.get("status", "error"),
        )
        return home()


if Config.CHANGE_GET_DATA_BY_WEB:
    get_data_web: GetDataWeb = GetDataWeb()
else:
    get_data_web: None = None  # CHƯA PHÁT TRIỂN GET DATA BY GOOGLE SHEET
