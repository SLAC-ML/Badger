from abc import ABC, abstractmethod
from typing import List, Dict, Optional, Any
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
        elif func.__name__ == 'set_values':
            if 'channel_inputs' in kwargs.keys():
                channel_inputs = kwargs['channel_inputs']
            else:
                channel_inputs = args[1]
            args[0]._logs.append({
                'timestamp': curr_ts().timestamp(),
                'action': 'set_values',
                'channel_inputs': channel_inputs,
            })

            return func(*args, **kwargs)
        elif func.__name__ == 'get_values':
            channel_outputs = func(*args, **kwargs)
            args[0]._logs.append({
                'timestamp': curr_ts().timestamp(),
                'action': 'get_values',
                'channel_outputs': channel_outputs,
            })

            return channel_outputs
        else:
            return func(*args, **kwargs)

    return func_log


class Interface(BaseModel, ABC):

    # name: str = Field(..., allow_mutation=False)
    name: str
    params: Optional[Dict] = Field({}, description='Interface parameters')
    _logs: List[Dict] = []

    class Config:
        underscore_attrs_are_private = True

    def get_value(self, channel: str):
        pass

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

    # Environment should only call this method to get channels
    def get_values(self, channel_names: List[str]) -> Dict[str, Any]:
        channel_outputs = {}
        for c in channel_names:
            channel_outputs[c] = self.get_value(c)

        return channel_outputs

    # Environment should only call this method to set channels
    def set_values(self, channel_inputs: Dict[str, Any]):
        for c, v in channel_inputs.items():
            self.set_value(c, v)
