from app.base import GetData
from app.schema.confession import ConfessionSchema
from app.services.save_cfs.save_cfs import SaveConfession as Confession
from app.utils.return_home import home
from app.validation.check_input_data import check_input_data
from app.schema.ReturnSchema import ReturnSchema
from configs import Config

from flask import flash, Response

import uuid
import time

__all__ = ["get_data_web"]


class GetDataWeb(GetData):

    @check_input_data
    def get_data(self, email: str = "", confession: str = "") -> Response:

        data = ConfessionSchema(
            confession=confession,
            email=email,
            confession_id=str(uuid.uuid4()),
            post_time=int(time.time()),
        )

        res: ReturnSchema = Confession.save_cfs(data)

        flash(res.msg, res.status)
        return home()


if Config.CHANGE_GET_DATA_BY_WEB:
    get_data_web: GetDataWeb = GetDataWeb()
else:
    get_data_web: None = None  # CHƯA PHÁT TRIỂN GET DATA BY GOOGLE SHEET
