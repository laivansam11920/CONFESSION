from concurrent.futures import ThreadPoolExecutor
from configs import Config

executor = ThreadPoolExecutor(max_workers=Config.MAX_THREADPOOLEXECUTOR_WORKER)
