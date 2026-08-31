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

__all__ = ["get_data_web", "get_data_google"]


class GetDataWeb(GetData):

    @check_input_data
    def get_data(self, email: str = "", confession: str = "") -> Response:

        data = ConfessionSchema(
            confession=confession,
            email=[
                email,
            ],
            confession_id=str(uuid.uuid4()),
            post_time=int(time.time()),
        )

        res: ReturnSchema = Confession.save_cfs(data)

        flash(res.msg, res.status)
        return home()

class GetDataGoogleForm(GetData):

    @check_input_data
    def get_data(self, email: str = "", confession: str = "") -> Response: ...


if Config.CHANGE_GET_DATA_BY_WEB:
    get_data_web: GetData = GetDataWeb()

if Config.CHANGE_GET_DATA_BY_GOOGLE_FORM:
    get_data_google: GetData = GetDataGoogleForm()
