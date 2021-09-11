from coolname import generate_slug
from ..factory import get_algo, get_env
from ..utils import config_list_to_dict, normalize_config_vars, \
    load_config, yprint, merge_params


def run_test(args):
    Environment, configs_env = get_env(args.env)
    optimize, configs_algo = get_algo(args.algo)
    configs_routine = load_config(args.config)
    try:
        routine_name = configs_routine['name']
    except KeyError:
        routine_name = generate_slug(2)
    params_env = load_config(args.env_params)
    params_algo = load_config(args.algo_params)
    params_algo = merge_params(configs_algo['params'], params_algo)

    # TODO: Sanity check here

    yprint(configs_routine)

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
            'options': params_algo,
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
