from app.database import db
from app.schema.ReturnSchema import ReturnSchema
from app.utils.get_cfs_count import cfs_nums
from configs import Config

import functools


class UpdateStatusModerationCfs:

    @staticmethod
    def update_cfs_moderation(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):

            res: ReturnSchema = func(*args, **kwargs)

            if not Config.MODERATION_CONFESSION:
                return res

            if not res.success:
                return res

            data = (
                db.docs.find_one(
                    {
                        "confession_id": res.data.get("confession_id"),
                        "send": False,
                        "status": "approved",
                        "set_status_moderation": False,
                    },
                    {"_id": 0, "ai_data": 1},
                )
                or {}
            )

            flag = False

            ai_data = data.get("ai_data", {})
            score = ai_data.get("score")

            if ai_data["uncertain"]:
                # In process
                ...

            if score and score > Config.MAX_MODERATION_SCORE:
                flag = True

            db.docs.update_one(
                {"confession_id": res.data.get("confession_id")},
                {
                    "$set": {
                        "safe_to_post": flag,
                        "set_status_moderation": True,
                        "cfs": cfs_nums(),
                    }
                },
            )

            return res

        return wrapper
