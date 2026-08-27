from pymongo import MongoClient
from pymongo.errors import ConnectionFailure, ServerSelectionTimeoutError

from configs import Config
from app.utils.logger import console

__all__ = ["Database"]


class Database:

    @staticmethod
    def connect():
        try:
            client: MongoClient[Any] = MongoClient(
                Config.MONGO_URI,
                timeoutMS=5000,
                serverSelectionTimeoutMS=5000,
                maxIdleTimeMS=45000,
            )
            client.admin.command("ping")
            return client[Config.MONGO_MAIN_DB]
        except (ConnectionFailure, ServerSelectionTimeoutError, Exception) as e:
            console.error(e)

    @staticmethod
    def create_index():
        pass
