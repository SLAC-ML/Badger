import os

import pandas as pd
import pytest
from xopt import VOCS
from xopt.generators import RandomGenerator


class TestRoutine:
    def create_routine(self):
        from badger.routine import Routine

        test_routine = {
            "name": "routine-for-core-test",
            "algo": "upper_confidence_bound",
            "env": "test",
            "algo_params": {
                "gp_constructor": {
                    "name": "standard",
                    "use_low_noise_prior": True,
                 },
                "beta": 2.0,
                "start_from_current": True,
            },
            "env_params": {},
            "config": {
                "variables":
                    {
                        "x0": [-1, 1],
                        "x1": [-1, 1],
                        "x2": [-1, 1],
                        "x3": [-1, 1]
                    },
                "objectives": {"f": "MAXIMIZE"},
                "init_points": {"x0": [0.5], "x1": [0.5], "x2": [0.5], "x3": [0.5]},
            },
        }

        vocs = VOCS(
            variables=test_routine["config"]["variables"],
            objectives=test_routine["config"]["objectives"],
        )

        generator = RandomGenerator(vocs=vocs)

        return Routine(
            name="test",
            vocs=vocs,
            generator=generator,
            environment_name="test",
            initial_points=pd.DataFrame(test_routine["config"]["init_points"])
        )

    def test_routine_init(self):
        routine = self.create_routine()
        routine.evaluate_data(routine.initial_points)

        assert len(routine.data) == 1

    def test_routine_serialization(self):
        from badger.routine import Routine

        routine = self.create_routine()
        routine.evaluate_data(routine.initial_points)
        routine.dump("test.yaml")

        lroutine = Routine.from_file("test.yaml")
        assert lroutine.environment.variable_names == routine.environment.variable_names
        lroutine.evaluate_data(routine.initial_points)

        assert len(lroutine.data) == 2

    @pytest.fixture(scope="module", autouse=True)
    def clean_up(self):
        yield
        files = ["test.yml"]
        for f in files:
            if os.path.exists(f):
                os.remove(f)
