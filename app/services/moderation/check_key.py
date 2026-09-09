from app.database import db
from app.utils.logger import console
from app.utils.return_home import home_moderation
from configs import Config

import functools
from datetime import datetime, timezone

from flask import request


class CheckKeyModerationService:

    @staticmethod
    def check(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            try:

                if not Config.SEND_MAIL:
                    return home_moderation()

                token = request.args.get("token")

                if not token:
                    return home_moderation()

                res = (
                    db.token_moderation.find_one_and_delete(
                        {
                            "token_moderation.key_moderation": token,
                            "token_moderation.expire_time": {
                                "$gte": datetime.now(timezone.utc),
                            },
                        },
                        {"_id": 0, "confession_id": 1},
                    )
                    or {}
                )

                if not res:
                    return home_moderation()

                return func(cfs_id=res.get("confession_id", ""), *args, **kwargs)

            except Exception as e:
                console.error(e)
                return home_moderation()

        return wrapper
