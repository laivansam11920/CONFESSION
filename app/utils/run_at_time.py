from app.extensions.ap_scheduler import scheduler
from typing import Callable

def run_at_time(time: int, /, func: Callable, method: str,  *args, **kwargs) -> None:
    scheduler.add_job(func, method, seconds=time, *args, **kwargs)
    scheduler.start()

