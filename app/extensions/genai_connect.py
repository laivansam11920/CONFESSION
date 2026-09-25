from google.genai import types, Client

from configs import Config
from app.utils.logger import console

__all__ = ["client"]

try:
    client: Client = Client(
        api_key=Config.GOOGLE_AI_API_KEY,
    )
except Exception as e:
    console.error(e)