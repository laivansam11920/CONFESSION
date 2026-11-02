from dataclasses import dataclass, field
from uuid import UUID, uuid4

__all__ = ["ConfessionDataSchema"]


@dataclass(kw_only=True, slots=True)
class ConfessionDataSchema:

    cfs_id: UUID = field(default_factory=uuid4)
    cfs_content: str

    @property
    def get_id_str(self) -> str:
        return str(self.cfs_id)
