from abc import ABC, abstractmethod
from typing import List, Dict
from pydantic import Field, BaseModel
import pickle
from .utils import curr_ts


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


class Interface(BaseModel, ABC):

    # name: str = Field(..., allow_mutation=False)
    name: str
    params: Dict = Field({}, description='Interface parameters')
    _logs: List[Dict] = []

    class Config:
        underscore_attrs_are_private = True

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
