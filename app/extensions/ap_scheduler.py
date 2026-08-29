from apscheduler.schedulers.background import BackgroundScheduler
import pytz

tz = pytz.timezone("Asia/Ho_Chi_Minh")
scheduler = BackgroundScheduler(timezone=tz)
