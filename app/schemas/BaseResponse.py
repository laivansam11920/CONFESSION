from dataclasses import dataclass

__all__ = ["BaseResponse"]


@dataclass(kw_only=True, slots=True)
class BaseResponse:
    success: bool
    msg: str
    status_code: int