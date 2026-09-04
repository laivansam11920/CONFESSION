import functools

from flask import flash, request
from email_validator import EmailNotValidError, validate_email
from flask_babel import Babel, gettext as _

from app.utils.logger import console
from app.utils.return_home import home
from app.middleware.check_max_len import check_max_len
from app.middleware.check_vip_token import is_vip_token
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

            max_len: int = Config.MAX_LEN_CONFESSION_ALLOW
            min_len: int = Config.MIN_LEN_CONFESSION_ALLOW
            is_sponsor: bool = False

            if key_vip and Config.VIP_ALLOW and is_vip_token(key_vip) :
                is_sponsor = True
                max_len = Config.MAX_LEN_CONFESSION_VIP_ALLOW
                min_len = Config.MIN_LEN_CONFESSION_VIP_ALLOW

            res_check_len = check_max_len(confession, max_len, min_len)

            if not res_check_len.success:
                flash(res_check_len.msg, "error")
                return home()

            return func(
                email=email,
                confession=confession,
                is_sponsor=is_sponsor,
                *args,
                **kwargs
            )
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
