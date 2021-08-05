import numpy as np
from abc import ABC, abstractmethod
from interface import Interface

class Environment(ABC):

    @property
    @abstractmethod
    def name(self) -> str:
        pass

    @property
    @abstractmethod
    def params(self):
        pass

    @property
    @abstractmethod
    def interface(self) -> Interface:
        pass

    @abstractmethod
    def get_current_x(self) -> np.ndarray:
        pass

    @abstractmethod
    def evaluate(self, X: np.ndarray) -> np.ndarray:
        pass
