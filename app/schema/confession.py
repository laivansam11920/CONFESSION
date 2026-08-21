from dataclasses import dataclass

@dataclass(frozen=True)
class ConfessionSchema:
    confession: str
    active: bool
    confession_id: str
    post_time: int
