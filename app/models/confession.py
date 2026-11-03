from dataclasses import dataclass, field
from uuid import UUID, uuid4
from datetime import datetime, timezone

__all__ = ["ConfessionDataSchema"]


@dataclass(kw_only=True, slots=True)
class ConfessionDataSchema:

    cfs_id: UUID = field(default_factory=uuid4)
    cfs_content: str
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))

    @property
    def get_id_str(self) -> str:
        return str(self.cfs_id)
