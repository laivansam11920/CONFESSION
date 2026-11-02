from .BaseResponse import BaseResponse

from dataclasses import dataclass
from typing import Any

__all__ = ['ErrorResponse']

@dataclass(kw_only=True, slots=True)
class ErrorResponse(BaseResponse):
    success: bool = False
    msg: str = "An unexpected error occurred!"
    status_code: int = 500
    error_code: str = "INTERNAL_SERVER_ERROR"
    details: dict[str, Any] | None = None
