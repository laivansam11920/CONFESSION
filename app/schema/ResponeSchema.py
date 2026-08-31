from pydantic import BaseModel, Field
from dataclasses import dataclass

__all__ = [
    "ConfessionItemResult",
    "ConfessionItem",
]


class ConfessionItem(BaseModel):
    score: float = Field(description="số điểm [số thập phân, ví dụ: 12.5]")
    reason: str = Field(
        description="lý do [1–2 câu, nêu rõ vi phạm hoặc lý do được điểm cao, không dài hơn 30 từ]"
    )
    propose: str = Field(
        description="propose: 'Nêu đề xuất chỉnh sửa dựa trên câu gốc'"
    )
    uncertain: bool = Field(
        description="Nếu không chắc chắn với kết quả, đầu ra sẽ là True và ngược lại, nếu hoàn toàn chắc chắn với kết quả thì đầu ra là False"
    )


@dataclass(frozen=True, slots=True)
class ConfessionItemResult:
    score: float| None = None
    reason: str = ""
    propose: str = ""
    uncertain: bool = True
