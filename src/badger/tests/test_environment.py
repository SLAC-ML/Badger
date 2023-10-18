import json
from typing import Optional, Dict, List

from pydantic import SerializeAsAny

from badger.environment import Environment
from badger.routine import Routine
from xopt.resources.testing import TEST_VOCS_BASE


class TestEnvironment(Environment):
    name = 'test'
    variables = {f'x{i}': [-1, 1] for i in range(20)}
    observables = ['f']

    my_flag: int = 0

    def set_variables(self, variable_inputs: Dict[str, float]):
        pass

    def get_observables(self, observable_names: List[str]) -> Dict:
        return {ele: 1.0 for ele in observable_names}


class TestEnv:
    def test_basic_env(self):
        env = TestEnvironment()
        result = dict(env)
        assert result["my_flag"] == 0

        env.my_flag = 1
        result = dict(env)
        assert result["my_flag"] == 1

        result = json.loads(env.json())
        assert result["my_flag"] == 1

    def test_env_in_routine(self):
        env = TestEnvironment()
        vocs = TEST_VOCS_BASE

        routine = Routine(
            name="test_routine",
            environment=env,
            vocs=vocs,
            generator="random"
        )
        result = json.loads(routine.json())
        assert result["environment"]["my_flag"] == 0

        routine.environment.my_flag = 1
        result = json.loads(routine.json())
        assert result["environment"]["my_flag"] == 1

