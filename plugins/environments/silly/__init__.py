import numpy as np
from badger import environment
from badger.interface import Interface
from operator import itemgetter

class Environment(environment.Environment):

    name = 'silly'

    def __init__(self, interface: Interface, params):
        super().__init__(interface, params)

    def get_x(self):
        d = itemgetter('dimension')(self.params)
        channels = [f'c{i + 1}' for i in range(d)]
        x = np.array(self.interface.get_values(channels))

        return x

    def set_x(self, x: np.ndarray):
        d = itemgetter('dimension')(self.params)
        channels = [f'c{i + 1}' for i in range(d)]
        self.interface.set_values(channels, x.tolist())

    def get_y(self):
        y = np.array(self.interface.get_values(['norm']))

        return y
