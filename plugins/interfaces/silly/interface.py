from ....badger import interface
from operator import itemgetter
import logging

class Interface(interface.Interface):

    name = 'silly'

    def __init__(self, params):
        super().__init__(params)

        prefix, count = itemgetter('channel_prefix', 'channel_count')(params)

        self.states = {}
        for i in range(count):
            self.states[f'{prefix}{i + 1}'] = 0

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
        except KeyError:
            logging.warn(f'Channel {channel} doesn\'t exist!')
