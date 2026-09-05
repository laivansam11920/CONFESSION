from app.base import GetData
from app.schema.confession import ConfessionSchema
from app.services.save_cfs.save_cfs import SaveConfession as Confession
from app.utils.return_home import home
from app.validation.check_input_data import check_input_data
from app.schema.ReturnSchema import ReturnSchema
from configs import Config

from flask import flash, Response, request

import uuid
import time

__all__ = ["get_data_web", "get_data_google"]


class GetDataWeb(GetData):

    @check_input_data
    def get_data(
        self,
        email: str = "",
        confession: str = "",
        is_sponsor: bool = False,
        post_time_reqs: str = "",
        use_tag_cfs_reqs: str = "",
    ) -> Response:

        data = ConfessionSchema(
            confession=confession,
            email=[
                email,
            ],
            confession_id=str(uuid.uuid4()),
            post_time=int(time.time()),
            is_sponsor=is_sponsor,
            sponsor_requirements={
                "post_time_reqs": post_time_reqs,
                "use_tag_cfs_reqs": use_tag_cfs_reqs,
            },
        )

        res: ReturnSchema = Confession.save_cfs(data)

        flash(res.msg, res.status)
        return home()


class GetDataGoogleForm(GetData):

    @check_input_data
    def get_data(
        self,
        email: str = "",
        confession: str = "",
        is_sponsor: bool = False,
        post_time_reqs: str = "",
        use_tag_cfs_reqs: str = "",
    ) -> tuple[dict, int]:

        data = ConfessionSchema(
            confession=confession,
            email=[
                email,
            ],
            confession_id=str(uuid.uuid4()),
            post_time=int(time.time()),
            is_sponsor=is_sponsor,
            sponsor_requirements={
                "post_time_reqs": post_time_reqs,
                "use_tag_cfs_reqs": use_tag_cfs_reqs,
            },
        )

        res: ReturnSchema = Confession.save_cfs(data)

        return {"success": res.success, "msg": res.msg}, 200


if Config.CHANGE_GET_DATA_BY_WEB:
    get_data_web: GetData = GetDataWeb()

if Config.CHANGE_GET_DATA_BY_GOOGLE_FORM:
    get_data_google: GetData = GetDataGoogleForm()
