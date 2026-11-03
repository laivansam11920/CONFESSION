from typing import Any, Optional

from app.schemas.ErrorResponse import ErrorResponse

__all__ = ["BaseAppException"]


class BaseAppException(Exception):

    message: str
    status_code: int
    error_code: str
    payload: Optional[dict[str, Any]]

    def __init__(
        self,
        message: str = "An unexpected error occurred.",
        status_code: int = 500,
        error_code: str = "INTERNAL_SERVER_ERROR",
        payload: Optional[dict[str, Any]] = None,
    ) -> None:
        self.message = message
        self.status_code = status_code
        self.error_code = error_code
        self.payload = payload or {}

    def to_response(self) -> ErrorResponse:
        return ErrorResponse(
            msg=self.message,
            status_code=self.status_code,
            error_code=self.error_code,
            details=self.payload or None,
        )
