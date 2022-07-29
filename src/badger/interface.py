from abc import ABC, abstractmethod
from typing import List
import pickle
from .utils import merge_params, curr_ts


def log(func):

    def func_log(*args, **kwargs):
        if func.__name__ == 'set_value':
            if 'channel' in kwargs.keys():
                channel = kwargs['channel']
            else:
                channel = args[1]
            if 'value' in kwargs.keys():
                value = kwargs['value']
            else:
                value = args[2]
            args[0]._logs.append({
                'timestamp': curr_ts().timestamp(),
                'action': 'set_value',
                'channel': channel,
                'value': value,
            })

            return func(*args, **kwargs)
        elif func.__name__ == 'get_value':
            if 'channel' in kwargs.keys():
                channel = kwargs['channel']
            else:
                channel = args[1]
            value = func(*args, **kwargs)
            args[0]._logs.append({
                'timestamp': curr_ts().timestamp(),
                'action': 'get_value',
                'channel': channel,
                'value': value,
            })

            return value
        else:
            return func(*args, **kwargs)

    return func_log


class Interface(ABC):

    @property
    @abstractmethod
    def name(self) -> str:
        pass

    @abstractmethod
    def __init__(self, params=None):
        self.params = merge_params(self.get_default_params(), params)
        self._logs = []

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

    def start_recording(self):
        self._logs = []

    def stop_recording(self, filename):
        # Do not create the pickle file if log is empty
        # This usually happens when the log decorator is not used in the
        # specific interface
        if not self._logs:
            return

        with open(filename, 'wb') as f:
            pickle.dump(self._logs, f)

        self._logs = []

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
