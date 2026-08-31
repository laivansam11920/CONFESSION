from abc import ABC, abstractmethod
from typing import Any


class AiServices(ABC):
    def __init__(self, client: Any, model: str):
        self.client = client
        self.model = model

    @abstractmethod
    def get_response(self, contents_input: str):
        pass


class GetData(ABC):

    @abstractmethod
    def get_data(self, email: str, confession: str):
        pass
