from app.extensions.ap_scheduler import scheduler
from typing import Callable

def run_at_time(time: int, /, func: Callable):
    scheduler.add_job(func, "interval", seconds=time)
    scheduler.start()

