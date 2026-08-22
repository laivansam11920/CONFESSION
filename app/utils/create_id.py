import unicodedata
import re
from hashlib import sha512


def generate_confession_id(text: str) -> str:

    text = text.lower()

    text = unicodedata.normalize("NFD", text)
    text = "".join([c for c in text if not unicodedata.combining(c)])

    text = re.sub(r"[^a-zA-Z0-9]", "", text)

    encrypt_text = sha512(text.encode("utf-8")).hexdigest()

    return encrypt_text
