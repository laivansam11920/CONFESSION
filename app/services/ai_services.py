from abc import ABC, abstractmethod

class AiServices(ABC):

    @abstractmethod
    def check_confession(self, text: str) -> bool:
        pass


