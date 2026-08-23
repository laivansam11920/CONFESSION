from pydantic import BaseModel, Field
from typing import List

__all__ = ["ConfessionModerationResponse"]


class ConfessionItem(BaseModel):
    score: int = Field(description="số điểm [số thập phân, ví dụ: 12.5]")
    reason: str = Field(
        description="lý do [1–2 câu, nêu rõ vi phạm hoặc lý do được điểm cao, không dài hơn 30 từ]"
    )
    propose: str = Field(
        description="propose: 'Nêu đề xuất chỉnh sửa dựa trên câu gốc'"
    )
    origin_text: str = Field(description="bản gốc chưa qua chỉnh sửa của confession")
    uncertain: bool = Field(
        description="Nếu không chắc chắn với kết quả, đầu ra sẽ là True và ngược lại, nếu hoàn toàn chắc chắn với kết quả thì đầu ra là False"
    )
    id_origin: str = Field(description="id gốc của confession chưa qua chỉnh sửa.")


class ConfessionModerationResponse(BaseModel):
    results: List[ConfessionItem]
