from app.database import db
from app.schema.ReturnSchema import ReturnSchema
from app.utils.get_cfs_count import cfs_nums
from app.services.send_mail.mail_services import Email
from configs import Config

import functools

__all__ = ["UpdateStatusModerationCfs"]


class UpdateStatusModerationCfs:

    @staticmethod
    def update_cfs_moderation(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):

            res: ReturnSchema = func(*args, **kwargs)

            if not res.success:
                return res

            cfs_id = res.data.get("confession_id")

            data = (
                db.docs.find_one(
                    {
                        "confession_id": cfs_id,
                        "send": False,
                        "status": "approved",
                    },
                    {"_id": 0, "ai_data": 1, "email": 1},
                )
                or {}
            )

            ai_data = data.get("ai_data", {})
            score = ai_data.get("score")
            email = data.get("email")

            if ai_data.get("uncertain") and email:
                if not Config.SEND_MAIL:
                    return res
                Email.send_mail(email=email, confession_id=cfs_id)
                return res

            # TODO: phát triển cơ chế thông báo nếu cfs vi phạm bằng session
            if score and score > Config.MAX_MODERATION_SCORE:
                db.docs.update_one(
                    {"confession_id": res.data.get("confession_id")},
                    {"$set": {"safe_to_post": True, "cfs": cfs_nums()}},
                )

            return res

        return wrapper
