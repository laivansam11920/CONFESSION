from flask_wtf.csrf import CSRFProtect

from app.utils.logger import console

__all__ = ["crfs"]

try:
    crfs = CSRFProtect()
except Exception as e:
    console.error(e)
