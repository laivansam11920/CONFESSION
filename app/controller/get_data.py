from app.base import GetData
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
    def get_data(self, email: str="", confession: str="") -> Response:

        data = ConfessionSchema(
            confession=confession,
            email=email,
            confession_id=str(uuid.uuid4()),
            post_time=int(time.time()),
        )

        res = SaveConfession.save_to_db(data)

        msg = res.get("msg") or _(
            "Rất tiếc, quá trình xử lý gặp chút sự cố. Bạn vui lòng thử lại sau nhé."
        )

        flash(msg, res.get("status", "error"))
        return home()


if Config.CHANGE_GET_DATA_BY_WEB:
    get_data_web: GetDataWeb = GetDataWeb()
else:
    get_data_web: None = None  # CHƯA PHÁT TRIỂN GET DATA BY GOOGLE SHEET
