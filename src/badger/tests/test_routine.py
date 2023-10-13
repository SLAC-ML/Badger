import pandas as pd
from xopt import VOCS, Evaluator
from xopt.generators import RandomGenerator


class TestRoutine:
    def test_routine_init(self):
        from badger.routine import Routine

        test_routine = {
            "name": "routine-for-core-test",
            "algo": "upper_confidence_bound",
            "env": "test",
            "algo_params": {
                "model": None,
                "turbo_controller": None,
                "use_cuda": False,
                "gp_constructor": {
                    "name": "standard",
                    "use_low_noise_prior": True,
                    "covar_modules": {},
                    "mean_modules": {},
                    "trainable_mean_keys": [],
                },
                "numerical_optimizer": {
                    "name": "LBFGS",
                    "n_restarts": 20,
                    "max_iter": 2000,
                },
                "max_travel_distances": None,
                "fixed_features": None,
                "n_candidates": 1,
                "n_monte_carlo_samples": 128,
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
                "constraints": None,
                "states": None,
                "domain_scaling": None,
                "tags": None,
                "init_points": {"x0": [0.5], "x1": [0.5], "x2": [0.5], "x3": [0.5]},
            },
        }

        vocs = VOCS(
            variables=test_routine["config"]["variables"],
            objectives=test_routine["config"]["objectives"],
        )

        generator = RandomGenerator(vocs=vocs)

        routine = Routine(
            name="test",
            vocs=vocs,
            generator=generator,
            environment_name="test",
            initial_points=pd.DataFrame(test_routine["config"]["init_points"])
        )
        routine.evaluate_data(routine.initial_points)

        assert len(routine.data) == 1

    def test_routine_serialization(self):
        routine = create_routine()
        routine.evaluate_data(routine.initial_points)

        routine.dump("test.yaml")

        loaded_routine = Routine.from_file("test.yaml")
        assert loaded_routine.environment == routine.environment
        loaded_routine.evaluate_data(routine.initial_points)
