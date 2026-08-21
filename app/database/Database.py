from pymongo import MongoClient
from pymongo.errors import ConnectionFailure, ServerSelectionTimeoutError

from configs import Config
from app.utils.logger import logger

__all__ = ["Database"]


class Database:

    @staticmethod
    def connet():
        try:
            client = MongoClient(
                Config.MONGO_URI,
                timeoutMS=5000,
                serverSelectionTimeoutMS=5000,
                maxIdleTimeMS=45000,
            )
            client.admin.command("ping")
            print("Connected")
            return client[Config.MONGO_MAIN_DB]
        except (ConnectionFailure, ServerSelectionTimeoutError, Exception) as e:
            logger.error(e)

    @staticmethod
    def create_index():
        pass
