from typing import Any, Optional

from app.schemas.ErrorResponse import ErrorResponse

class BaseAppException(Exception):

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

    def to_dict(self) -> ErrorResponse:
        return ErrorResponse(
            msg=self.message,
            status_code=self.status_code,
            error_code=self.error_code,
            details=self.payload or None,
        )