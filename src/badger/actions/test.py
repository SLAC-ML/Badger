import os
import numpy as np
import matplotlib.pyplot as plt
from coolname import generate_slug
from ..factory import get_algo, get_env
from ..utils import config_list_to_dict, normalize_config_vars, \
    load_config, yprint

# Temp fix for the duplicated MP lib error
os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"


def run_test(args):
    Environment, configs_env = get_env(args.env)
    optimize, configs_algo = get_algo(args.algo)
    configs_routine = load_config(args.config)
    try:
        routine_name = configs_routine['name']
    except KeyError:
        routine_name = generate_slug(2)
    _configs_env = load_config(args.env_config)
    if _configs_env:
        configs_env = {**configs_env, **_configs_env}
    _configs_algo = load_config(args.algo_config)
    if _configs_algo:
        configs_algo = {**configs_algo, **_configs_algo}

    # TODO: Sanity check here

    yprint(configs_routine)

    params_env = {
        'params': configs_env['params'],
        'variables': configs_env['variables'],
        'observations': configs_env['observations'],
    }
    env = Environment(None, params_env)

    def evaluate(inputs, extra_option='abc', **params):
        env.set_vars_dict(inputs)
        outputs = env.get_obses_dict()

        return outputs

    config = {
        'xopt': {
            'output_path': None,
            'verbose': True,
        },
        'algorithm': {
            'name': configs_algo['name'],
            'options': configs_algo['params'],
        },
        'simulation': {
            'name': configs_env['name'],
            'evaluate': evaluate,
        },
        'vocs': {
            'name': routine_name,
            'description': None,
            'simulation': configs_env['name'],
            'templates': None,
            'variables': config_list_to_dict(normalize_config_vars(configs_routine['variables'])),
            'objectives': config_list_to_dict(configs_routine['objectives']),
            'constraints': config_list_to_dict(configs_routine['constraints']),
        }
    }

    results = optimize(config)
    print('done!')

    # Plotting
    # fig, ax = plt.subplots()
    # variables = results['variables']
    # valid = results['variables'][results['feasibility'].flatten()]
    # ax.plot(variables[:, 0], variables[:, 1], '-o', label='all')
    # ax.plot(valid[:, 0], valid[:, 1], 'o', label='valid')
    # ax.set_xlabel('$x_1$')
    # ax.set_ylabel('$x_2$')
    # ax.legend()
    # plt.show()
