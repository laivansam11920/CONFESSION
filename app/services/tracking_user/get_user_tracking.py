from app.database import db
from app.schema.ReturnSchema import ReturnSchema
from app.utils.logger import console
from app.utils.get_client_ip import get_client_ip
from app.utils.encrypt import encrypt_data
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
                "user_tracking_data.ip": str(encrypt_data(kwargs["data"]["ip"])),
                "user_tracking_data.fingerprint": str(
                    encrypt_data(kwargs["data"]["fingerprint"])
                ),
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

                user_ip: str = get_client_ip()
                fingerprint_id: str = request.form.get("fingerprint_id", "")

                user_tracking_data: dict[str, Any] = {
                    "ip": user_ip,
                    "fingerprint": fingerprint_id,
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
