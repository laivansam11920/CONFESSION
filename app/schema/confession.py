# docs: docs/ConfessionSchema.md
from dataclasses import dataclass, field


@dataclass(frozen=True)
class ConfessionSchema:
    confession: str
    confession_id: str
    post_time: int
    email: str
    same_post_count: int = 0
    is_moderation_post: bool = False
    status: str = "pending"
    send: bool = False
    ai_data: dict = field(default_factory=dict)
