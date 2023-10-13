import copy
from typing import Optional, Dict, List

import numpy as np
import pandas as pd
from pandas import DataFrame
from pydantic import BaseModel, ConfigDict, Field
from xopt import Generator, VOCS
from xopt.generators import get_generator

from badger.environment import Environment, instantiate_env
from badger.factory import get_env
from badger.utils import merge_params


class Routine(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)

    name: str
    environment: Environment
    generator: Generator
    initial_points: DataFrame
    data: Optional[DataFrame] = Field(None, description="internal DataFrame object")
    tags: Optional[Dict] = Field(None)

    # convenience properties
    @property
    def vocs(self):
        """
        A property that returns the vocs of the generator attribute.

        Returns:
            self.generator.vocs : VOCS
        """
        return self.generator.vocs

    def add_data(self, new_data):
        # Set internal dataframe.
        if self.data is not None:
            new_data = pd.DataFrame(new_data, copy=True)  # copy for reindexing
            new_data.index = np.arange(
                len(self.data) + 1, len(self.data) + len(new_data) + 1
            )

            self.data = pd.concat([self.data, new_data], axis=0)
        else:
            self.data = new_data
        self.generator.add_data(new_data)


def build_routine(
        routine_name: str,
        vocs: VOCS,
        algo_name: str,
        algo_params: dict,
        env_name: str,
        env_params: dict,
        init_points: pd.DataFrame,
        tags: List[str]
):
    """ build routine object from configuration dict """
    generator_class = get_generator(algo_name)
    generator = generator_class(
        vocs=vocs, **copy.deepcopy(algo_params)
    )

    env_class, configs_env = get_env(env_name)
    _configs_env = merge_params(
        configs_env, {'params': env_params})
    environment = instantiate_env(env_class, _configs_env)

    return Routine(
        name=routine_name,
        environment=environment,
        generator=generator,
        initial_points=init_points,
        tags=tags
    )
