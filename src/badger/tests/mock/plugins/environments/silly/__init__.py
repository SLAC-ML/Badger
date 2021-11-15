import numpy as np
from badger import environment
from badger.interface import Interface


class Environment(environment.Environment):

    name = 'silly'
    var_channel_map = {
        'q1': 'c1',
        'q2': 'c2',
        'q3': 'c3',
        'q4': 'c4',
    }

    def __init__(self, interface: Interface, params):
        super().__init__(interface, params)

    @staticmethod
    def list_vars():
        return ['q1', 'q2', 'q3', 'q4']

    @staticmethod
    def list_obses():
        return ['l1', 'l2']

    @staticmethod
    def get_default_params():
        return None

    def _get_var(self, var):
        return self.interface.get_value(self.var_channel_map[var])

    def _set_var(self, var, x):
        self.interface.set_value(self.var_channel_map[var], x)

    def _get_obs(self, obs):
        if obs == 'l1':
            values = self.interface.get_values(
                ['c1', 'c2', 'c3', 'c4', 'c5', 'c6'])
            return np.sum(np.abs(values))
        elif obs == 'l2':
            return self.interface.get_value('norm')
