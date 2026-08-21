from dataclasses import dataclass

@dataclass(frozen=True)
class ConfessionSchema:
    confession: str
    authors: list[str]
    active: bool
    confession_id: str
    post_time: dict[str, int]
    same_post_count: int = 0
