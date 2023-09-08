import pytest
from unittest.mock import Mock, patch
from ..core import run_routine_xopt, instantiate_env, Routine, evaluate_points
from pandas import DataFrame
from ..factory import get_env
from ..utils import range_to_str, yprint, merge_params, ParetoFront, norm, denorm, \
     parse_rule
from xopt.generators import get_generator

class result:
    pass 

@pytest.fixture
def mock_dependencies():
    with patch('..core.get_env') as get_env,\
         patch('..utils.merge_params') as merge_params,\
         patch('..core.instantiate_env') as instantiate_env,\
         patch('xopt.generators.get_generator') as get_generator,\
         patch('pandas.DataFrame.from_dict') as from_dict,\
         patch('..core.Routine') as Routine,\
         patch('..utils.ParetoFront') as ParetoFront,\
         patch('..core.evaluate_points') as evaluate_points:

        # Yield a dictionary of mocks to the test function
        yield {
            'get_env': get_env,
            'merge_params': merge_params,
            'instantiate_env': instantiate_env,
            'get_generator': get_generator,
            'DataFrame': from_dict,
            'Routine': Routine,
            'ParetoFront': ParetoFront,
            'evaluate_points': evaluate_points
        }



def test_run_routine_xopt(mock_dependencies):
    data_buffer = []

    def mock_evaluate_callback(data: DataFrame):
        data_buffer.append(data)

    mock_active_callback = Mock()
    mock_generate_callback = Mock()
    mock_pf_callback = Mock()
    mock_states_callback = Mock()

    test_routine = {
        "name": "routine-for-core-test",
        "algo": "upper_confidence_bound",
        "env": "sphere",
        "algo_params": {
            "model": None,
            "turbo_controller": None,
            "use_cuda": False,
            "model_constructor": {
                "name": "standard",
                "use_low_noise_prior": True,
                "covar_modules": {},
                "mean_modules": {},
                "trainable_mean_keys": [],
            },
            "numerical_optimizer": {
                "name": "LBFGS",
                "n_raw_samples": 20,
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
        "init_points": {"x0": [0.5], "x1": [0.5], "x2": [0.5], "x3": [0.5]},
        },
    }

    mock_dependencies['get_env'].return_value = ('Environment', 'configs_env')
    mock_dependencies['merge_params'].return_value = {'params': 'merged_params'}
    mock_dependencies['get_generator'].return_value = 'GeneratorClass'

    # Call the function to test
    run_routine_xopt(
        test_routine, 
        mock_active_callback, 
        mock_generate_callback, 
        mock_evaluate_callback, 
        mock_pf_callback, 
        mock_states_callback
    )

    # Assertions to verify that the mocks were called as expected
    mock_dependencies['get_env'].assert_called_once_with('sphere')
    mock_dependencies['merge_params'].assert_called_once_with('configs_env', {'params': {}})
    mock_dependencies['instantiate_env'].assert_called_once_with('Environment', {'params': 'merged_params'})
    mock_dependencies['get_generator'].assert_called_once_with('upper_confidence_bound')
    mock_dependencies['DataFrame'].assert_called_once_with({"x0": [0.5], "x1": [0.5], "x2": [0.5], "x3": [0.5]})
    mock_dependencies['Routine'].assert_called_once()
    mock_dependencies['ParetoFront'].assert_called_once()

    # asserts output is what is expected 
    # just compare objectives 


