import json
import yaml
from typing import Optional, List, Any

import pandas as pd
from pandas import DataFrame
from pydantic import ConfigDict, Field, model_validator, field_validator, \
    FieldValidationInfo, SerializeAsAny
from xopt import Xopt, VOCS, Evaluator
from xopt.generators import get_generator

from badger.environment import Environment, instantiate_env
from badger.factory import get_env


class Routine(Xopt):
    model_config = ConfigDict(arbitrary_types_allowed=True)

    name: str
    environment: SerializeAsAny[Environment]
    initial_points: Optional[DataFrame] = Field(None)
    critical_constraint_names: Optional[List[str]] = Field(None)
    tags: Optional[List] = Field(None)
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

            # validate data (if it exists
            if "data" in data:
                if isinstance(data["data"], dict):
                    try:
                        data["data"] = pd.DataFrame(data["data"])
                    except IndexError:
                        data["data"] = pd.DataFrame(data["data"], index=[0])

                    data["generator"].add_data(data["data"])

            # instantiate env
            if isinstance(data["environment"], dict):
                # TODO: Actually we need this interface info, but
                # should be put somewhere else (in parallel with env?)
                try:
                    del data["environment"]["interface"]
                except KeyError:  # no interface at all, which is good
                    pass
                name = data["environment"].pop("name")
                env_class, configs_env = get_env(name)
                data["environment"] = instantiate_env(
                    env_class, data["environment"] | configs_env
                )
            else:  # should be an instantiated env already
                pass

            # create evaluator
            env = data["environment"]

            def evaluate_point(point: dict):
                env._set_variables(point)
                obs = env._get_observables(data["vocs"].objective_names)

                return obs

            data["evaluator"] = Evaluator(function=evaluate_point)

        return data

    @field_validator("initial_points", mode="before")
    def validate_data(cls, v, info: FieldValidationInfo):
        if isinstance(v, dict):
            try:
                v = pd.DataFrame(v)
            except IndexError:
                v = pd.DataFrame(v, index=[0])

        return v

    def json(self, **kwargs) -> str:
        """Handle custom serialization of environment"""

        print(self.environment)

        result = super().json(**kwargs)
        dict_result = json.loads(result)

        print(dict_result, 'routine json')

        # Remove extra fields
        # extra_fields = [
        #     "data"
        # ]
        # dict_result.pop('no exist')
        # dict_result["environment"].pop()
        # try:
        #     del dict_result["data"]
        # except KeyError:
        #     pass
        # try:
        #     del dict_result["dump_file"]
        # except KeyError:
        #     pass
        # try:
        #     del dict_result["evaluator"]
        # except KeyError:
        #     pass
        # try:
        #     del dict_result["max_evaluations"]
        # except KeyError:
        #     pass
        # try:
        #     del dict_result["serialize_inline"]
        # except KeyError:
        #     pass
        # try:
        #     del dict_result["serialize_torch"]
        # except KeyError:
        #     pass
        # try:
        #     del dict_result["strict"]
        # except KeyError:
        #     pass

        dict_result["environment"] = {"name": self.environment.name} |\
            dict_result["environment"]

        return json.dumps(dict_result)
