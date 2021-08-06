from ....badger import interface
import logging

class Interface(interface.Interface):

    name = 'silly'
    states = {
        'c1': 0,
        'c2': 1,
        'c3': 2,
        'c4': 3
    }

    def get_values(self, channels: list[str]) -> list:
        values = []
        for c in channels:
            try:
                values.append(self.states[c])
            except KeyError:
                values.append(None)

        return values

    def set_values(self, channels: list[str], values: list):
        assert len(channels) == len(values), 'Channels and values number mismatch!'

        for idx, c in enumerate(channels):
            try:
                self.states[c] = values[idx]
            except KeyError:
                logging.warn(f'Channel {c} doesn\'t exist!')
