from app.extensions.ap_scheduler import scheduler
from app.utils.logger import console
from typing import Callable


def run_at_time(time: int, /, func: Callable, method: str = "cron", *args, **kwargs) -> bool:
    try:
        scheduler.add_job(func, method, second=time, *args, **kwargs)
        scheduler.start()
        return True
    except Exception as e:
        console.error(e)
        return False
