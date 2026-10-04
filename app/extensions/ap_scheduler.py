from apscheduler.schedulers.background import BackgroundScheduler
import pytz

from app.utils.logger import console
from configs import Config

try:
    tz = pytz.timezone(Config.TIME_ZONE)
    scheduler = BackgroundScheduler(timezone=tz)
except Exception as e:
    console.error(e)
