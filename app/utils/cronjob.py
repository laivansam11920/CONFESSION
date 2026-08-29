from configs import Config
from app.utils.logger import console
from app.services.post_cfs.post_facebook import Facebook

from time import sleep
from requests import get

def self_ping():
    while True:
        sleep(10 * 60)
        if Config.RENDER_EXTERNAL_URL:
            try:
                get(f"{Config.RENDER_EXTERNAL_URL}/ping", timeout=10)
            except Exception as e:
                console.error(e)

def my_daily_task():
    try:
        Facebook.post()
    except Exception as e:
        console.error(e)