from abc import ABC, abstractmethod
from typing import Any

from configs import Config


class AiServices(ABC):
    def __init__(self, client: Any, model: str):
        self.client = client
        self.model = model

    @abstractmethod
    def get_response(self, contents_input: str):
        pass


class GetData(ABC):

    @abstractmethod
    def get_data(self, email: str = "", confession: str = ""):
        pass

class PostFacebook(ABC):

    def __init__(self):
        self.page_id = Config.FACEBOOK_PAGE_ID
        self.page_access_token = Config.FACEBOOK_PAGE_ACCESS_TOKEN

    @abstractmethod
    def post(self):
        pass