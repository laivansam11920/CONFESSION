from dataclasses import dataclass


@dataclass
class ConfessionDataSchema:
    confession_id: int
    confession_content: str
