from apscheduler.schedulers.background import BackgroundScheduler
import pytz

from configs import Config

tz = pytz.timezone(Config.TIME_ZONE)
scheduler = BackgroundScheduler(timezone=tz)
