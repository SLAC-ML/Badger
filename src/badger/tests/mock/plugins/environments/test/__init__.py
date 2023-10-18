import torch
from typing import Dict, List, Optional
from badger import environment
from badger.errors import BadgerNoInterfaceError


class Environment(environment.Environment):

    name = 'test_w_interface'
    variables = {f'x{i}': [-1, 1] for i in range(20)}
    observables = ['f']

    flag: Optional[int] = 0

    def set_variables(self, variable_inputs: Dict[str, float]):
        if not self.interface:
            raise BadgerNoInterfaceError

        self.interface.set_values(variable_inputs)
        full_outputs = self.interface.get_values(self.variable_names)

        # Filling up the observations
        x = torch.tensor([full_outputs[f'x{i}'] for i in range(20)])
        self.interface.set_value('f', (x ** 2).sum().numpy())

    def get_observables(self, observable_names: List[str]) -> Dict:
        return {ele: 1.0 for ele in observable_names}
