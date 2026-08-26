from app.base import ConfessionManager
from app.utils.logger import console
from .save_tracking_data import save_tracking_id
from configs import Config

import functools
from typing import Any

from flask import request
from app.extensions.threads import executor

__all__ = ["tracking_service"]


class TrackingService(ConfessionManager):

    def save_user_tracking(self, func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            try:
                res = func(*args, **kwargs)

                if not Config.TRACKING_USER:
                    return res

                user_ip = request.remote_addr
                user_fingerprint_id = request.form.get("user_fingerprint_id")

                user_tracking_data: dict[str, Any] = {
                    "ip": user_ip,
                    "fingerprint": user_fingerprint_id,
                }

                if res.get("success", False):
                    confession_id = res["data"]["confession_id"] or None
                    if confession_id is None:
                        return res
                    executor.submit(
                        lambda: save_tracking_id(
                            self.db,
                            confession_id=confession_id,
                            data=user_tracking_data,
                        )
                    )
                    return res
                return res
            except Exception as e:
                console.error(e)

        return wrapper


tracking_service = TrackingService()
