from concurrent.futures import ThreadPoolExecutor

from app.utils.logger import console
from configs import Config

try:
    executor = ThreadPoolExecutor(max_workers=Config.MAX_THREADPOOL_EXECUTOR_WORKER)
except Exception as e:
    console.error(e)
