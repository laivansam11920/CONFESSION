# docs: docs/ConfessionSchema.md
from dataclasses import dataclass, field

__all__ = ["ConfessionSchema"]


@dataclass(frozen=True)
class ConfessionSchema:
    confession: str
    confession_id: str
    post_time: int
    email: list
    admin_comment: str = ""
    safe_to_post: bool = False
    same_post_count: int = 0
    status: str = "pending"
    send: bool = False
    ai_data: dict = field(default_factory=dict)
    user_tracking_data: list[str] = field(default_factory=list)
