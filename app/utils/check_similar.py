import re
from rapidfuzz import fuzz

def normalize_text(text: str) -> str:
    text = text.lower().strip()
    text = re.sub(r"[^\w\s]", "", text)
    return text


def is_similar(text1: str, text2: str, similarity_threshold: int) -> bool:
    score = fuzz.ratio(normalize_text(text1), normalize_text(text2))
    return score >= similarity_threshold
