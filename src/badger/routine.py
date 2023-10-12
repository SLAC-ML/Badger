import copy

from pandas import DataFrame
from pydantic import BaseModel, ConfigDict
from xopt import Generator
from xopt.generators import get_generator

from badger.core import instantiate_env
from badger.environment import Environment
from badger.factory import get_env
from badger.utils import merge_params


class Routine(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)

    environment: Environment
    generator: Generator
    initial_points: DataFrame

    # convenience properties
    @property
    def vocs(self):
        """
        A property that returns the vocs of the generator attribute.

        Returns:
            self.generator.vocs : VOCS
        """
        return self.generator.vocs


def build_routine(routine_config: dict):
    """ build routine object from configuration dict """

    Environment, configs_env = get_env(routine_config['env'])
    _configs_env = merge_params(
        configs_env, {'params': routine_config['env_params']})
    environment = instantiate_env(Environment, _configs_env)

    variables = {key: value for dictionary in routine_config['config']['variables']
                 for key, value in dictionary.items()}
    objectives = {key: value for dictionary in routine_config['config']['objectives']
                  for key, value in dictionary.items()}
    vocs = {
        'variables': variables,
        'objectives': objectives,
    }
    generator_class = get_generator(routine_config['algo'])
    try:
        del routine_config['algo_params']['start_from_current']
    except KeyError:
        pass
    routine_copy = copy.deepcopy(routine_config['algo_params'])
    # Note! The following line will remove all the name fields in
    # generator params. That's why we make a copy here so the modification
    # will not affect the routine to be saved (in archive)
    generator = generator_class(vocs=vocs, **routine_copy)

    try:
        initial_points = routine_config['config']['init_points']
        initial_points = DataFrame.from_dict(initial_points)
        if initial_points.empty:
            raise KeyError
    except KeyError:  # start from current
        initial_points = environment.get_variables(generator.vocs.variable_names)
        initial_points = DataFrame(initial_points, index=[0])

    routine = Routine(environment=environment, generator=generator,
                           initial_points=initial_points)

    return routine
