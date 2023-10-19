import pandas as pd
from xopt import VOCS
from xopt.generators import RandomGenerator


class TestDB:
    @staticmethod
    def create_routine():
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
            environment={"name": "test"},
            initial_points=pd.DataFrame(test_routine["config"]["init_points"])
        )

    def test_save_routine(self):
        from badger.db import save_routine, remove_routine

        routine = self.create_routine()
        save_routine(routine)

        remove_routine("test")

    def test_load_routine(self):
        from badger.db import save_routine, load_routine, remove_routine

        routine = self.create_routine()
        save_routine(routine)

        new_routine, time = load_routine("test")
        assert new_routine.generator == routine.generator
        assert new_routine.vocs == routine.vocs

        remove_routine("test")

