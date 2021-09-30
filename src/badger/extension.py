import numpy as np
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

    # Run an optimization on the given environment
    @abstractmethod
    def run(self, env, configs: dict):
        pass
