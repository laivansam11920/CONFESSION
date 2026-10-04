from flask_babel import Babel

from app.utils.logger import console

__all__ = ["babel"]

try:
    babel: Babel = Babel()
except Exception as e:
    console.error(e)
