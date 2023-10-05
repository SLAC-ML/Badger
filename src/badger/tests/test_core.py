import os
import copy
import pytest
import pandas as pd
from typing import Type
from xopt.generators import get_generator
from badger.utils import merge_params, ParetoFront
from badger.core import (
    run_routine_xopt,
    evaluate_points,
    Routine,
    instantiate_env,
)
from badger.errors import BadgerRunTerminatedError


class TestCore:
    """
    This class is to provide unit test coverage for the core.py file.
    """

    @pytest.fixture(autouse=True, scope="function")
    def test_core_setup(self, *args, **kwargs) -> None:
        super(TestCore, self).__init__(*args, **kwargs)
        self.count = 0
        self.points_eval = None
        self.candidates = None
        self.points_eval_list = []
        self.candidates_list = []
        self.states = None

        data = {"x0": [0.5], "x1": [0.5], "x2": [0.5], "x3": [0.5]}
        data_eval_target = {
            "x0": [0.5],
            "x1": [0.5],
            "x2": [0.5],
            "x3": [0.5],
            "f": [1.0],
        }

        self.points = pd.DataFrame(data)

        self.points_eval_target = pd.DataFrame(data_eval_target)

        self.test_evaluate_points_cases = [
            (
                self.points,
                self.mock_routine,
                self.mock_evaluate_points_callback,
                self.points_eval_target,
            )
        ]

    def mock_routine(self) -> Type[Routine]:
        """
        A method that creates a Routine class object
        filled with sample data for testing purposes.
        """
        from badger.factory import get_env

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
                "variables": [
                    {"x0": [-1, 1]},
                    {"x1": [-1, 1]},
                    {"x2": [-1, 1]},
                    {"x3": [-1, 1]},
                ],
                "objectives": [{"f": "MAXIMIZE"}],
                "constraints": None,
                "states": None,
                "domain_scaling": None,
                "tags": None,
                "init_points": {
                    "x0": [0.5],
                    "x1": [0.5],
                    "x2": [0.5],
                    "x3": [0.5],
                },
            },
        }

        # Initialize routine
        Environment, configs_env = get_env(test_routine["env"])
        _configs_env = merge_params(
            configs_env, {"params": test_routine["env_params"]}
        )
        environment = instantiate_env(Environment, _configs_env)

        variables = {
            key: value
            for dictionary in test_routine["config"]["variables"]
            for key, value in dictionary.items()
        }
        objectives = {
            key: value
            for dictionary in test_routine["config"]["objectives"]
            for key, value in dictionary.items()
        }
        vocs = {
            "variables": variables,
            "objectives": objectives,
        }

        generator_class = get_generator(test_routine["algo"])

        del test_routine["algo_params"]["start_from_current"]
        del test_routine["algo_params"]["n_candidates"]
        del test_routine["algo_params"]["fixed_features"]

        test_routine_copy = copy.deepcopy(test_routine["algo_params"])

        generator = generator_class(vocs=vocs, **test_routine_copy)

        initial_points = test_routine["config"]["init_points"]
        initial_points = pd.DataFrame.from_dict(initial_points)

        test_routine_xopt = Routine(
            environment=environment,
            generator=generator,
            initial_points=initial_points,
        )

        return test_routine_xopt

    def mock_active_callback(self) -> int:
        """
        A mock active callback method to test
        if active callback is functioning properly.
        """
        if self.count >= 5:
            return 2
        else:
            return 0

    def mock_generate_callback(self, candidates: pd.DataFrame) -> None:
        """
        A mock generate callback method to test
        if generate callback is functioning properly.
        """
        self.candidates_list.append(candidates)

    def mock_evaluate_callback(self, points_eval: pd.DataFrame) -> None:
        """
        A mock evaluate callback method to test
        if evaluate callback is functioning properly.
        """
        self.points_eval_list.append(points_eval)
        self.count += 1

    def mock_pf_callback(self, pf: Type[ParetoFront]) -> None:
        """
        A mock pareto callback method to test
        if pareto callback is functioning properly.
        """
        self.pf = pf

    def mock_states_callback(self, states: dict) -> None:
        """
        A mock states callback method to test
        if states callback is functioning properly.
        """
        self.states = states

    def mock_dump_file_callback(self) -> str:
        """
        A mock dump file callback method to test
        if dump file callback is functioning properly.
        """
        return "test.yaml"

    def test_run_routine_xopt(self) -> None:
        """
        A unit test to ensure the core functionality
        of run_routine_xopt is functioning as intended.
        """
        routine = self.mock_routine()

        with pytest.raises(BadgerRunTerminatedError):
            run_routine_xopt(
                routine,
                self.mock_active_callback,
                self.mock_generate_callback,
                self.mock_evaluate_callback,
                self.mock_pf_callback,
                self.mock_states_callback,
                self.mock_dump_file_callback,
            )

        assert len(self.candidates_list) == self.count - 1
        assert len(self.points_eval_list) == self.count

        assert self.pf is not None
        assert self.states is None

        path = "./test.yaml"
        assert os.path.exists(path) is True
        os.remove("./test.yaml")

    def mock_evaluate_points_callback(self, points_eval: pd.DataFrame) -> None:
        """
        A mock callback method to test if callback method passed
        to the evaluate_points method is functioning properly.
        """
        self.points_eval = points_eval

    def test_evaluate_points(self) -> None:
        """
        A unit test to ensure the core functionality of evaluate_points
        is functioning as intended.
        """
        routine = self.mock_routine()

        assert routine.environment.get_variables(["x1", "x2"]) == {
            "x1": 0,
            "x2": 0,
        }
        evaluate_points_result = evaluate_points(
            self.points, routine, self.mock_evaluate_points_callback
        )

        assert evaluate_points_result.astype(float).equals(
            self.points_eval_target.astype(float)
        )
        assert self.points_eval.astype(float).equals(
            self.points_eval_target.astype(float)
        )
