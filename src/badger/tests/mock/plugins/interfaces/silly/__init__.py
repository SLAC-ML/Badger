import numpy as np
from badger import interface
from operator import itemgetter
import logging


class Interface(interface.Interface):

    name = 'silly'

    def __init__(self, params=None):
        super().__init__(params)

        prefix, count = itemgetter(
            'channel_prefix', 'channel_count')(self.params)

        self.channels = []
        self.states = {}
        for i in range(count):
            self.channels.append(f'{prefix}{i + 1}')
            self.states[f'{prefix}{i + 1}'] = 0

        self.channels.append('norm')
        self.states['norm'] = 0

    @staticmethod
    def get_default_params():
        return {
            'channel_prefix': 'c',
            'channel_count': 8
        }

    def get_value(self, channel: str):
        try:
            value = self.states[channel]
        except KeyError:
            logging.warning(f'Channel {channel} doesn\'t exist!')
            value = None

        return value

    def set_value(self, channel: str, value):
        if channel not in self.channels:
            logging.warning(f'Channel {channel} doesn\'t exist!')
            return

        try:
            self.states[channel] = value
            values = np.array([self.states[channel]
                              for channel in self.channels[:-1]])
            self.states['norm'] = np.sqrt(np.sum(values ** 2))
        except KeyError:
            logging.warning(f'Channel {channel} doesn\'t exist!')
