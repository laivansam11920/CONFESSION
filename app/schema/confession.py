# docs: docs/ConfessionSchema.md
from dataclasses import dataclass, field

__all__ = ["ConfessionSchema"]


@dataclass(frozen=True, slots=True)
class IpSchema:
    ip: list[str] = field(default_factory=list)


@dataclass(frozen=True, slots=True)
class FingerprintSchema:
    fingerprint: list[str] = field(default_factory=list)


@dataclass(frozen=True)
class ConfessionSchema:
    confession: str
    confession_id: str
    post_time: int
    email: str
    same_post_count: int = 0
    status: str = "pending"
    send: bool = False
    ai_data: dict = field(default_factory=dict)
    user_tracking_data: dict[IpSchema, FingerprintSchema] = field(default_factory=dict)
