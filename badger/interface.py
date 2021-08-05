from abc import ABC, abstractmethod

class Interface(ABC):

    @property
    @abstractmethod
    def name(self) -> str:
        pass

    @abstractmethod
    def get_values(self, channels: list[str]) -> list:
        pass

    @abstractmethod
    def set_values(self, channels: list[str], values: list):
        pass
