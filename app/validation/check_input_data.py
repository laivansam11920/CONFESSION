import functools

from flask import flash, request
from email_validator import EmailNotValidError, validate_email
from flask_babel import Babel, gettext as _

from app.utils.logger import logger
from app.utils.return_home import home
from configs import Config


def check_input_data(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        try:
            confession: str = request.form.get("confession", "")
            email: str = request.form.get("email", "anonymous")

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

            if len(confession) > Config.MAX_LEN_CONFESSION_ALLOW:
                flash(_("Confession của bạn quá dài!"), "error")
                return home()

            return func(email=email, confession=confession, *args, **kwargs)
        except EmailNotValidError:
            flash(_("Email của bạn không hợp lệ!"), "error")
            return home()
        except Exception as e:
            logger.error(e)
            flash(
                _(
                    "Rất tiếc, quá trình xử lý gặp chút sự cố. Bạn vui lòng thử lại sau nhé."
                ),
                "error",
            )
            return home()

    return wrapper
