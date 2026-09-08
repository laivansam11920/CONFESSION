from app.database import db
from app.utils.logger import console
from configs import Config

import functools

from flask import request, render_template
from pymongo import ReturnDocument


class CheckKeyModerationService:

    @staticmethod
    def check(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            try:

                if not Config.SEND_MAIL:
                    return render_template(
                        "moderation/action.html",
                        confession=None,
                        post_time=00.00,
                        score=0,
                        reason=None,
                    )

                token = request.args.get("token")

                if not token:
                    return render_template(
                        "moderation/action.html",
                        confession=None,
                        post_time=00.00,
                        score=0,
                        reason=None,
                    )

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
                    return render_template(
                        "moderation/action.html",
                        confession=None,
                        post_time=00.00,
                        score=0,
                        reason=None,
                    )
                return func(cfs_id=res.get("confession_id", ""), *args, **kwargs)

            except Exception as e:
                console.error(e)
                return func(key_success=False, cfs_id=0, *args, **kwargs)

        return wrapper
