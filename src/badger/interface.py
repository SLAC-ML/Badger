from abc import ABC, abstractmethod
from typing import List
from .utils import merge_params


class Interface(ABC):

    @property
    @abstractmethod
    def name(self) -> str:
        pass

    @abstractmethod
    def __init__(self, params=None):
        self.params = merge_params(self.get_default_params(), params)

    # Get the default params of the interface
    @staticmethod
    @abstractmethod
    def get_default_params() -> dict:
        pass

    @abstractmethod
    def get_value(self, channel: str):
        pass

    @abstractmethod
    def set_value(self, channel: str, value):
        pass

    def get_values(self, channels: List[str]) -> list:
        values = []
        for c in channels:
            values.append(self.get_value(c))

        return values

    def set_values(self, channels: List[str], values: list):
        assert len(channels) == len(
            values), 'Channels and values number mismatch!'

        for idx, c in enumerate(channels):
            self.set_value(c, values[idx])
