import numpy as np
import time
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
    def get_default_params() -> dict:
        return None

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

    # Check variable
    # Unsafe version
    def _check_var(self, var: str):
        # 0: success
        # other: error code
        return 0

    # Actions to preform after change vars and before read vars/obj
    def vars_changed(self, vars: List[str], values: list):
        pass

    # Get current system states
    # If return is not None, the states would be saved at the start of each run
    # Should return a dict if not None
    def get_system_states(self):
        return None

    # Get observation
    # Unsafe version
    @abstractmethod
    def _get_obs(self, obs: str):
        pass

    # Get variable range
    # Unsafe version
    def _get_vrange(self, var: str):
        return [0, 1]

    # Safe version of _get_vrange
    def get_vrange(self, var: str):
        if var not in self.list_vars():
            raise Exception(f'Variable {var} doesn\'t exist!')

        return self._get_vrange(var)

    # Get all the variable ranges
    def get_vranges(self, vars=None):
        if vars is None:
            return [self._get_vrange(var) for var in self.list_vars()]
        else:
            return [self.get_vrange(var) for var in vars]

    # Get all the variable ranges
    def get_vranges_dict(self, vars=None):
        book = {}
        if vars is None:
            vars = self.list_vars()
            for var in vars:
                book[var] = self._get_vrange(var)
        else:
            for var in vars:
                book[var] = self.get_vrange(var)
        return book

    # Safe version of _get_var
    def get_var(self, var: str):
        if var not in self.list_vars():
            raise Exception(f'Variable {var} doesn\'t exist!')

        return self._get_var(var)

    # Safe version of _set_var with check
    def set_var(self, var: str, x):
        if var not in self.list_vars():
            raise Exception(f'Variable {var} doesn\'t exist!')

        self._set_var(var, x)

        # Wait until check_var returns 0
        status = 1
        while status:
            status = self._check_var(var)
            time.sleep(0.1)

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

    # Unsafe version of get_vars
    def _get_vars(self, vars: List[str]) -> list:
        values = []
        for var in vars:
            values.append(self._get_var(var))

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

        # Wait until all check_var calls return 0
        status = np.ones(len(vars))
        while np.any(status):
            for idx, var in enumerate(vars):
                status[idx] = self._check_var(var)
            time.sleep(0.1)

    # Unsafe version of set_vars
    def _set_vars(self, vars: List[str], values: list):
        assert len(vars) == len(
            values), 'Variables and values number mismatch!'

        for idx, var in enumerate(vars):
            self._set_var(var, values[idx])

        # Wait until all check_var calls return 0
        status = np.ones(len(vars))
        while np.any(status):
            for idx, var in enumerate(vars):
                status[idx] = self._check_var(var)
            time.sleep(0.1)

    def set_vars_dict(self, book: dict):
        for var, val in book.items():
            self.set_var(var, val)

        # Wait until all check_var calls return 0
        status = np.ones(len(book))
        while np.any(status):
            for idx, var in enumerate(book.keys()):
                status[idx] = self._check_var(var)
            time.sleep(0.1)

    # Unsafe version of set_vars_dict
    def _set_vars_dict(self, book: dict):
        for var, val in book.items():
            self._set_var(var, val)

        # Wait until all check_var calls return 0
        status = np.ones(len(book))
        while np.any(status):
            for idx, var in enumerate(book.keys()):
                status[idx] = self._check_var(var)
            time.sleep(0.1)

    def get_obses(self, obses: List[str]) -> list:
        values = []
        for obs in obses:
            values.append(self.get_obs(obs))

        return values

    # Unsafe version of get_obses
    def _get_obses(self, obses: List[str]) -> list:
        values = []
        for obs in obses:
            values.append(self._get_obs(obs))

        return values

    def get_obses_dict(self) -> dict:
        obses = self.list_obses()
        book = {}
        for obs in obses:
            book[obs] = self._get_obs(obs)

        return book
