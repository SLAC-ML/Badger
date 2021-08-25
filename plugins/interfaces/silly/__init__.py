import numpy as np
from badger import interface
from operator import itemgetter
import logging

class Interface(interface.Interface):

    name = 'silly'

    def __init__(self, params):
        super().__init__(params)

        prefix, count = itemgetter('channel_prefix', 'channel_count')(params)

        self.channels = []
        self.states = {}
        for i in range(count):
            self.channels.append(f'{prefix}{i + 1}')
            self.states[f'{prefix}{i + 1}'] = 0

        self.channels.append('norm')
        self.states['norm'] = 0

    def get_value(self, channel: str):
        try:
            value = self.states[channel]
        except KeyError:
            logging.warn(f'Channel {channel} doesn\'t exist!')
            value = None

        return value

    def set_value(self, channel: str, value):
        try:
            self.states[channel] = value
            values = np.array([self.states[channel] for channel in self.channels[:-1]])
            self.states['norm'] = np.sqrt(np.sum(values ** 2))
        except KeyError:
            logging.warn(f'Channel {channel} doesn\'t exist!')
