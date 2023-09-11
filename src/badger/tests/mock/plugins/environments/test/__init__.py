import torch
from typing import Dict
from badger import environment


class Environment(environment.Environment):

    name = 'test'
    variables = {f'x{i}': [-1, 1] for i in range(20)}
    observables = ['f']

    def get_variables(self, variable_names):
        assert self.interface, 'Must provide an interface!'

        variable_outputs = self.interface.get_values(variable_names)

        return variable_outputs

    def set_variables(self, variable_inputs: Dict[str, float]):
        assert self.interface, 'Must provide an interface!'

        self.interface.set_values(variable_inputs)
        full_outputs = self.interface.get_values(self.variable_names)

        # Filling up the observations
        x = torch.tensor([full_outputs[f'x{i}'] for i in range(20)])
        self.interface.set_value('f', (x ** 2).sum().numpy())

    def get_observables(self, observable_names):
        assert self.interface, 'Must provide an interface!'

        return self.interface.get_values(observable_names)
