from dataclasses import dataclass

__all__ = ["BaseResponse"]


@dataclass(kw_only=True, slots=True, frozen=True)
class BaseResponse:
    success: bool = False
    msg: str = "An unexpected error occurred!"
    code: int = 500
