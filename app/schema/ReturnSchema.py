from dataclasses import dataclass, field
from flask_babel import Babel, gettext as _

@dataclass(frozen=True)
class ReturnSchema:
    success: bool = False
    msg: str = _("Rất tiếc, có chút sự cố nhỏ khi lưu confession. Bạn thử lại giúp chúng mình nha.")
    status: str = "error"
    data: dict[str, str] = field(default_factory=dict)