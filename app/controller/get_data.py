from base import GetData
from app.services.save_data import SaveConfession
from app.schema.confession import ConfessionSchema

from flask import request, flash, redirect, url_for

import uuid
import time

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

        flash(res.get("msg", ""), res.get("status", "error"))
        return redirect(url_for('main_route.index'))

get_data_web = GetDataWeb()