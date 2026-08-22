from difflib import SequenceMatcher
import re

from configs import Config


def normalize_text(text: str) -> str:
    text = text.lower().strip()
    text = re.sub(r"[^\w\s]", "", text)
    return text


def is_similar(text1: str, text2: str) -> bool:
    ratio = SequenceMatcher(None, normalize_text(text1), normalize_text(text2)).ratio()
    return ratio >= Config.SIMILARITY_THRESHOLD