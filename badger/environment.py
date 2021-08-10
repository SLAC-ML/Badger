import numpy as np
from abc import ABC, abstractmethod
from interface import Interface

class Environment(ABC):

    @property
    @abstractmethod
    def name(self) -> str:
        pass

    @abstractmethod
    def __init__(self, interface: Interface, params):
        self.interface = interface
        self.params = params

    @abstractmethod
    def get_x(self) -> np.ndarray:
        pass

    @abstractmethod
    def set_x(self, x: np.ndarray):
        pass

    @abstractmethod
    def get_y(self) -> np.ndarray:
        pass

    def evaluate(self, X: np.ndarray) -> np.ndarray:
        Y = []
        for x in X:
            self.set_x(x)
            y = self.get_y()
            Y.append(y)
        Y = np.array(Y)

        return Y
