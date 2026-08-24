import functools

from flask import flash, request
from email_validator import EmailNotValidError, validate_email
from flask_babel import Babel, gettext as _
from markupsafe import escape

from app.utils.logger import logger
from app.utils.return_home import home
from configs import Config



def check_input_data(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        try:
            confession: str = request.form.get("confession", "")
            email: str = request.form.get("email", "anonymous")

            confession = escape(confession)

            if not confession or not confession.strip():
                flash(_("Confession không được để trống hoặc chỉ chứa khoảng trắng!"), "error")
                return home()

            if len(confession) > Config.MAX_LEN_CONFESSION_ALLOW:
                flash(_("Confession của bạn quá dài!"), "error")
                return home()

            validate_email(email, check_deliverability=False)

            return func(email=email, confession=confession, *args, **kwargs)
        except (EmailNotValidError, Exception) as e:
            logger.error(e)
            flash(_("Email của bạn không hợp lệ!"), "error")
            return home()
    return wrapper
