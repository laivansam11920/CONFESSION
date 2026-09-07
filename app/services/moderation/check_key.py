from app.database import db
from app.utils.logger import console
from configs import Config

import functools

from flask import request
from pymongo import ReturnDocument


class CheckKeyModerationService:

    @staticmethod
    def check(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            try:

                if not Config.SEND_MAIL:
                    return func(key_success=False, *args, **kwargs)

                token = request.args.get("token")

                if not token:
                    return func(key_success=False, *args, **kwargs)

                res = (
                    db.docs.find_one_and_update(
                        {"key_moderation": token},
                        {"$set": {"key_moderation": "used"}},
                        {"_id": 0, "confession_id": 1},
                        return_document=ReturnDocument.AFTER,
                    )
                    or {}
                )

                if not res:
                    return func(key_success=False, *args, **kwargs)
                return func(key_success=True, cfs_id=res.get("confession_id", ""), *args, **kwargs)

            except Exception as e:
                console.error(e)
                return func(key_success=False, *args, **kwargs)
        return wrapper
