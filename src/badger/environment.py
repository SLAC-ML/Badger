import numpy as np
from abc import ABC, abstractmethod
from typing import List
from .interface import Interface
from .utils import merge_params


class Environment(ABC):

    @property
    @abstractmethod
    def name(self) -> str:
        pass

    @abstractmethod
    def __init__(self, interface: Interface, params=None):
        self.interface = interface
        self.params = merge_params(self.get_default_params(), params)

    # List all available variables
    @staticmethod
    @abstractmethod
    def list_vars() -> List[str]:
        pass

    # List all available observations
    @staticmethod
    @abstractmethod
    def list_obses() -> List[str]:
        pass

    # Get the default params of the environment
    @staticmethod
    @abstractmethod
    def get_default_params() -> dict:
        pass

    # Get current variable
    # Unsafe version (var won't be checked beforehand)
    @abstractmethod
    def _get_var(self, var: str):
        pass

    # Set variable
    # Unsafe version
    @abstractmethod
    def _set_var(self, var: str, x):
        pass

    # Get observation
    # Unsafe version
    @abstractmethod
    def _get_obs(self, obs: str):
        pass

    # Get variable range
    # Unsafe version
    @classmethod
    def _get_vrange(cls, var: str):
        return [0, 1]

    # Safe version of _get_vrange
    @classmethod
    def get_vrange(cls, var: str):
        if var not in cls.list_vars():
            raise Exception(f'Variable {var} doesn\'t exist!')

        return cls._get_vrange(var)

    # Get all the variable ranges
    @classmethod
    def get_vranges(cls, vars=None):
        if vars is None:
            return [cls._get_vrange(var) for var in cls.list_vars()]
        else:
            return [cls.get_vrange(var) for var in vars]

    # Get all the variable ranges
    @classmethod
    def get_vranges_dict(cls, vars=None):
        book = {}
        if vars is None:
            vars = cls.list_vars()
            for var in vars:
                book[var] = cls._get_vrange(var)
        else:
            for var in vars:
                book[var] = cls.get_vrange(var)
        return book

    # Safe version of _get_var
    def get_var(self, var: str):
        if var not in self.list_vars():
            raise Exception(f'Variable {var} doesn\'t exist!')

        return self._get_var(var)

    # Safe version of _set_var
    def set_var(self, var: str, x):
        if var not in self.list_vars():
            raise Exception(f'Variable {var} doesn\'t exist!')

        return self._set_var(var, x)

    # Safe version of _get_obs
    def get_obs(self, obs: str):
        if obs not in self.list_obses():
            raise Exception(f'Observation {obs} doesn\'t exist!')

        return self._get_obs(obs)

    def get_vars(self, vars: List[str]) -> list:
        values = []
        for var in vars:
            values.append(self.get_var(var))

        return values

    def get_vars_dict(self) -> dict:
        vars = self.list_vars()
        book = {}
        for var in vars:
            book[var] = self._get_var(var)

        return book

    def set_vars(self, vars: List[str], values: list):
        assert len(vars) == len(
            values), 'Variables and values number mismatch!'

        for idx, var in enumerate(vars):
            self.set_var(var, values[idx])

    def set_vars_dict(self, book: dict):
        for var, val in book.items():
            self.set_var(var, val)

    def get_obses(self, obses: List[str]) -> list:
        values = []
        for obs in obses:
            values.append(self._get_obs(obs))

        return values

    def get_obses_dict(self) -> dict:
        obses = self.list_obses()
        book = {}
        for obs in obses:
            book[obs] = self.get_obs(obs)

        return book
