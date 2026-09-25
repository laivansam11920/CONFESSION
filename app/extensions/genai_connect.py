from google.genai import types, Client

from configs import Config

__all__ = ["client"]

client: Client = Client(
    api_key=Config.GOOGLE_AI_API_KEY,
    http_options=types.HttpOptions(timeout=50000),
)
