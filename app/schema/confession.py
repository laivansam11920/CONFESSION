# docs: docs/ConfessionSchema.md
from dataclasses import dataclass, field

__all__ = ["ConfessionSchema"]


@dataclass(frozen=True)
class DataRequirements:
    post_time_reqs: int
    use_tag_cfs_reqs: bool = False


@dataclass(frozen=True)
class ConfessionSchema:
    confession: str
    confession_id: str

    post_time: int
    admin_comment: str = ""

    email: list[str] = field(default_factory=list)
    same_post_count: int = 0

    safe_to_post: bool = False
    status: str = "pending"
    send: bool = False
    is_sponsor: bool = False
    sponsor_requirements: dict = field(default_factory=dict)

    ai_data: dict[str, int | bool] = field(default_factory=dict)
    user_tracking_data: list[str] = field(default_factory=list)
