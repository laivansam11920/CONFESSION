import re
from rapidfuzz import fuzz


def normalize_text(text: str, on: bool) -> str:
    if not on:
        return text
    text = text.lower().strip()
    text = re.sub(r"[^\w\s]", "", text)
    return text


def is_similar(
    text1: str,
    text2: str,
    /,
    similarity_threshold: float,
    on_normalize_text: bool,
) -> bool:
    score = fuzz.ratio(
        normalize_text(text1, on_normalize_text),
        normalize_text(text2, on_normalize_text),
    )
    return score >= similarity_threshold
