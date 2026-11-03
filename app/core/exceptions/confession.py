from uuid import UUID

from .base import BaseAppException

__all__ = [
    "ConfessionNotFoundException",
]


class ConfessionNotFoundException(BaseAppException):
    def __init__(self, cfs_id: UUID | None = None) -> None:
        msg: str = (
            f"Confession with ID '{cfs_id}' was not found."
            if cfs_id
            else "Confession not found."
        )
        super().__init__(
            message=msg,
            status_code=404,
            error_code="CONFESSION_NOT_FOUND",
            payload={"cfs_id": str(cfs_id)} if cfs_id else None,
        )
