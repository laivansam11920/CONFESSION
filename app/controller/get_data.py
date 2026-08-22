from base import GetData
from app.schema.confession import ConfessionSchema
from app.services.save_data import SaveConfession

from flask import request, flash, redirect, url_for
from flask_babel import Babel, gettext as _

import uuid
import time

__all__ = ["get_data_web"]

class GetDataWeb(GetData):

    def get_data(self):

        confession: str = request.form.get('confession', "")
        email: str = request.form.get('email', "anonymous")

        data = ConfessionSchema(
            confession=confession,
            email=email,
            confession_id=str(uuid.uuid4()),
            post_time=int(time.time()),
        )

        res = SaveConfession.save_to_db(data)

        flash(res.get("msg", _("Đã xảy ra 1 lỗi nào đó")), res.get("status", "error"))
        return redirect(url_for('main_route.index'))


get_data_web: GetDataWeb = GetDataWeb()