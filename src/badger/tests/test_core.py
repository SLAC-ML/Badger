import pytest
from badger.core import (run_routine_xopt, preto_setup,  
    save_states, evaluate_initial_points, set_dump_file, Routine, instantiate_env)

import copy
from pandas import DataFrame
from badger.utils import merge_params
from badger.factory import get_env
from xopt.generators import get_generator

def mock_routine():
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
        # Initialize routine
    Environment, configs_env = get_env(test_routine['env'])
    _configs_env = merge_params(configs_env, {'params': test_routine['env_params']})
    environment = instantiate_env(Environment, _configs_env)

    # self.env_ready(environment)
    
    variables = {key: value for dictionary in test_routine['config']['variables']
                     for key, value in dictionary.items()}
    objectives = {key: value for dictionary in test_routine['config']['objectives']
                      for key, value in dictionary.items()}
    vocs = {
            'variables': variables,
            'objectives': objectives,
        }
    
    generator_class = get_generator(test_routine['algo'])
    
    try:
        del test_routine['algo_params']['start_from_current']
    except KeyError:
        pass
    
    del test_routine['algo_params']['n_candidates']
    del test_routine['algo_params']['fixed_features']

    test_routine_copy = copy.deepcopy(test_routine['algo_params'])

    generator = generator_class(vocs=vocs, **test_routine_copy)

    # TODO -- this need changing to remove try except
    try:
        initial_points = test_routine['config']['init_points']
        initial_points = DataFrame.from_dict(initial_points)
        if initial_points.empty:
                raise KeyError
    except KeyError:  # start from current
        initial_points = environment.get_variables(generator.vocs.variable_names)
        initial_points = DataFrame(initial_points, index=[0])

    test_routine_xopt = Routine(environment=environment, generator=generator,
                               initial_points=initial_points)
    
    return test_routine_xopt

test_preto_setup_cases = [
    (mock_routine(), "", True), 
    (mock_routine(), "", False) 
]

@pytest.mark.parametrize("routine, pf_callback, expected", test_preto_setup_cases)
def test_preto_setup(routine, pf_callback, expected):
    assert preto_setup(routine, pf_callback) == expected
 

test_save_states_cases = [
    ("", "", True), 
    ("", "", False)
]

@pytest.mark.parametrize("environment, states_callback, expected", test_save_states_cases)
def test_save_states(environment, states_callback, expected): 
    assert save_states(environment, states_callback) == expected
 

test_evaluate_initial_cases = [
    ("", mock_routine(), "", ""), 
    ("", mock_routine(), "", "")
]

@pytest.mark.parametrize("initial_points, routine, evaluate_callback, expected", test_evaluate_initial_cases)
def test_evaluate_initial_points(initial_points, routine, evaluate_callback, expected):
    assert evaluate_initial_points(initial_points, routine, evaluate_callback) == expected

test_set_dump_file_cases = [
    (None, type(None)), 
    (True, str), 
]

@pytest.mark.parametrize("dump_file_callback, expected_type", test_set_dump_file_cases)
def test_set_dump_file(dump_file_callback, expected_type):
    result = set_dump_file(dump_file_callback)
    assert isinstance(result, expected_type)

test_run_routine_xopt_cases = [
    (mock_routine(), "", "", "", "", "", "", ""), 
    (mock_routine(), "", "", "", "", "", "", "")
]

@pytest.mark.parametrize(
        "routine, active_callback, " \
        "generate_callback, evaluate_callback, " \
        "pf_callback, states_callback, " \
        "dump_file_callback, expected",  
        test_run_routine_xopt_cases)
def test_run_routine_xopt(
    routine, 
    active_callback, 
    generate_callback, 
    evaluate_callback, 
    pf_callback, 
    states_callback, 
    dump_file_callback, 
    expected):
    assert run_routine_xopt(routine, active_callback, generate_callback,
        evaluate_callback, pf_callback, states_callback, dump_file_callback) == expected

