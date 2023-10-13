from typing import Optional, List

from pandas import DataFrame
from pydantic import ConfigDict, Field
from xopt import Xopt

from badger.environment import Environment


class Routine(Xopt):
    model_config = ConfigDict(arbitrary_types_allowed=True)

    name: str
    environment: Environment
    initial_points: DataFrame
    tags: Optional[List] = Field(None)
    critical_constraint_names: Optional[List[str]] = Field(None)
    script: Optional[str] = Field(None)

