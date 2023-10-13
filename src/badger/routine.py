from typing import Optional, List, Any

from pandas import DataFrame
from pydantic import ConfigDict, Field, model_validator
from xopt import Xopt, VOCS, Evaluator
from xopt.generators import get_generator

from badger.environment import Environment, instantiate_env
from badger.factory import get_env


class Routine(Xopt):
    model_config = ConfigDict(arbitrary_types_allowed=True)

    name: str
    environment: Environment
    initial_points: DataFrame
    tags: Optional[List] = Field(None)
    critical_constraint_names: Optional[List[str]] = Field(None)
    script: Optional[str] = Field(None)

    @model_validator(mode="before")
    @classmethod
    def validate_model(cls, data: Any):
        if isinstance(data, dict):
            # validate vocs
            if isinstance(data["vocs"], dict):
                data["vocs"] = VOCS(**data["vocs"])

            # validate generator
            if isinstance(data["generator"], dict):
                name = data["generator"].pop("name")
                generator_class = get_generator(name)
                data["generator"] = generator_class.model_validate(
                    {**data["generator"], "vocs": data["vocs"]}
                )
            elif isinstance(data["generator"], str):
                generator_class = get_generator(data["generator"])

                data["generator"] = generator_class.model_validate(
                    {"vocs": data["vocs"]}
                )

            if isinstance(data["environment"], dict):
                env_class, configs_env = get_env(data["environment"].pop("name"))
                data["environment"] = instantiate_env(env_class, data["environment"])

            # create evaluator
            env = data["environment"]

            def evaluate_point(point: dict):
                env._set_variables(point)
                obs = env._get_observables(data["vocs"].observables)

                return obs

            data["evaluator"] = Evaluator(function=evaluate_point)

        return data
