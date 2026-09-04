from flask_babel import Babel, gettext as _
from app.schema.ReturnSchema import ReturnSchema


def check_max_len(text: str, max_len: int, min_len: int) -> ReturnSchema:
    l = len(text)

    if l > max_len:
        return ReturnSchema(
            success=False,
            msg=_("Confession của bạn quá dài so với yêu cầu hệ thống!"),
        )

    if l <= min_len:
        return ReturnSchema(
            success=False, msg=_("Confession của bạn quá ngắn so với yêu cầu hệ thống!")
        )

    return ReturnSchema(
        success=True,
    )
