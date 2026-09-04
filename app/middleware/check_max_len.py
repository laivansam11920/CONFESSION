from flask_babel import Babel, gettext as _
from app.schema.ReturnSchema import ReturnSchema
from app.utils.logger import console

def check_max_len(text: str, max_len: int, min_len: int) -> ReturnSchema:
    try:
        l = len(text)

        if l > max_len:
            return ReturnSchema(
                msg=_("Confession của bạn quá dài so với yêu cầu hệ thống!"),
            )

        if l <= min_len:
            return ReturnSchema(
                msg=_("Confession của bạn quá ngắn so với yêu cầu hệ thống!")
            )

        return ReturnSchema(
            success=True,
        )
    except Exception as e:
        console.error(e)
        return ReturnSchema()
