from app.database import db
from app.utils.logger import console
from app.schema.ReturnSchema import ReturnSchema
from configs import Config

import functools
from typing import Any

from flask import request
from app.extensions.threads import executor

__all__ = ["TrackingService"]


def save_tracking_id(**kwargs):
    db.docs.update_one(
        {"confession_id": kwargs["confession_id"]},
        {
            "$addToSet": {
                "user_tracking_data.ip": kwargs["data"]["ip"],
                "user_tracking_data.fingerprint": kwargs["data"]["fingerprint"],
            }
        },
    )


class TrackingService:

    @staticmethod
    def save_user_tracking(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            try:
                res: ReturnSchema = func(*args, **kwargs)

                if not Config.TRACKING_USER:
                    return res

                user_ip = request.remote_addr
                user_fingerprint_id = request.form.get("user_fingerprint_id")

                user_tracking_data: dict[str, Any] = {
                    "ip": user_ip,
                    "fingerprint": user_fingerprint_id,
                }

                if res.success:
                    confession_id = res.data.get("confession_id")
                    if confession_id is None:
                        return res
                    executor.submit(
                        lambda: save_tracking_id(
                            confession_id=confession_id,
                            data=user_tracking_data,
                        )
                    )
                    return res
                return res
            except Exception as e:
                console.error(e)

        return wrapper
