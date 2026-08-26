from dotenv import load_dotenv, find_dotenv
from app.utils.logger import console

__all__ = ["Config"]

if not load_dotenv(find_dotenv(), override=True):
    console.warning("No .env file found, using default config")

from .configs import Config
