import functools
from datetime import datetime, timezone

from flask import flash, request
from email_validator import EmailNotValidError, validate_email
from flask_babel import Babel, gettext as _

from app.utils.logger import console
from app.utils.return_home import home
from app.database import db
from configs import Config


def check_input_data(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        try:
            confession: str = request.form.get("confession", "")
            email: str = request.form.get("email", "anonymous")
            key_vip: str = request.form.get("key_vip", "")

            if email != "anonymous":
                validate_email(email, check_deliverability=False)

            if not confession or not confession.strip():
                flash(
                    _(
                        "Rất tiếc, hệ thống chưa nhận được nội dung confession của bạn. Vui lòng kiểm tra và gửi lại nhé!"
                    ),
                    "error",
                )
                return home()

            max_len = Config.MAX_LEN_CONFESSION_ALLOW
            min_len = Config.MIN_LEN_CONFESSION_ALLOW

            if key_vip and Config.VIP_CFS_ON:
                data = (
                    db.vip_key.find_one_and_update(
                        {
                            "key": key_vip,
                            "used": False,
                            "expires_at": {
                                "$lte": datetime.now(timezone.utc),
                            },
                        },
                        {
                            "$set": {
                                "used": True,
                            },
                        },
                        {"_id": 0, "used": 1},
                    )
                    or {}
                )
                if data.get("used", False):
                    max_len = Config.MAX_LEN_CONFESSION_VIP_ALLOW
                    min_len = Config.MIN_LEN_CONFESSION_VIP_ALLOW

            l = len(confession)

            if l > max_len:
                flash(_("Confession của bạn quá dài so với yêu cầu hệ thống!"), "error")
                return home()

            if l <= min_len:
                flash(
                    _("Confession của bạn quá ngắn so với yêu cầu hệ thống!"), "error"
                )
                return home()

            return func(email=email, confession=confession, *args, **kwargs)
        except EmailNotValidError:
            flash(_("Email của bạn không hợp lệ!"), "error")
            return home()
        except Exception as e:
            console.error(e)
            flash(
                _(
                    "Rất tiếc, quá trình xử lý gặp chút sự cố. Bạn vui lòng thử lại sau nhé."
                ),
                "error",
            )
            return home()

    return wrapper
