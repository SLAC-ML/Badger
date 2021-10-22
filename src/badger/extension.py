from abc import ABC, abstractmethod
from typing import List


class Extension(ABC):

    @property
    @abstractmethod
    def name(self) -> str:
        pass

    @abstractmethod
    def __init__(self):
        pass

    # List all available algorithms
    @abstractmethod
    def list_algo(self) -> List[str]:
        pass

    # Get config of an algorithm
    @abstractmethod
    def get_algo_config(self, name: str):
        pass

    # Run an optimization with an array-style evaluate function
    # and a configs dict
    @abstractmethod
    def optimize(self, evaluate, configs: dict):
        pass
