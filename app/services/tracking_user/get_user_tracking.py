from app.database import db
from app.schema.ReturnSchema import ReturnSchema
from app.utils.logger import console
from app.utils.get_client_tracking import get_client_tracking
from app.utils.encrypt import encrypt_data
from configs import Config

import functools

from app.extensions.threads import executor

__all__ = ["TrackingService"]


def save_tracking_id(**kwargs):
    db.docs.update_one(
        {"confession_id": kwargs["confession_id"]},
        {
            "$push": {
                "user_tracking_data": str(encrypt_data(kwargs["user_tracking"])),
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

                if res.success:
                    confession_id = res.data.get("confession_id")
                    if confession_id is None:
                        return res
                    executor.submit(
                        lambda: save_tracking_id(
                            confession_id=confession_id,
                            user_tracking=get_client_tracking(),
                        )
                    )
                    return res
                return res
            except Exception as e:
                console.error(e)

        return wrapper
