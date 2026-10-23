from app.database import db
from app.schema.ReturnSchema import ReturnSchema
from app.services.moderation.scan_pending_confessions import ModerationQueueScanner
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
                    },
                    {"_id": 0, "ai_data": 1, "email": 1},
                )
                or {}
            )

            ai_data = data.get("ai_data", {})
            email = data.get("email")

            if ai_data.get("uncertain", True) and email and Config.SEND_MAIL:
                Email.send_mail(email=email, confession_id=cfs_id)

            ModerationQueueScanner.scan(cfs_id)

            return res

        return wrapper
