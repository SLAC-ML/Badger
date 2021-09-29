import numpy as np
import sys
import logging
from coolname import generate_slug
from ..factory import get_algo, get_intf, get_env
from ..utils import load_config, yprint, merge_params


def run_routine(args):
    Environment, configs_env = get_env(args.env)
    try:
        intf_name = configs_env['interface'][0]
        Interface, _ = get_intf(intf_name)
        intf = Interface()
    except Exception:
        intf = None

    optimize, configs_algo = get_algo(args.algo)
    try:
        configs_routine = load_config(args.config)
    except Exception as e:
        logging.error(e)
        return
    try:
        routine_name = configs_routine['name']
    except KeyError:
        routine_name = generate_slug(2)
        configs_routine['name'] = routine_name
    try:
        params_env = load_config(args.env_params)
        params_algo = load_config(args.algo_params)
    except Exception as e:
        logging.error(e)
        return
    params_algo = merge_params(configs_algo['params'], params_algo)

    # TODO: Sanity check here

    yprint(configs_routine)

    env = Environment(intf, params_env)

    if not callable(optimize):
        configs = {
            'routine_configs': configs_routine,
            'algo_configs': merge_params(configs_algo, {'params': params_algo})
        }
        results = optimize.run(env, configs)
        print('done!')
    else:
        # Make a normalized evaluate function
        def evaluate(X):
            Y = []
            for x in X:
                env.set_vars(configs_routine['variables'], x)
                obses = []
                for obj in configs_routine['objectives']:
                    key = list(obj.keys())[0]
                    ptype = list(obj.values())[0]
                    obs = env.get_obs(key)
                    if ptype == 'MAXIMIZE':
                        obses.append(-obs)
                    else:
                        obses.append(obs)
                Y.append(obses)
            Y = np.array(Y)

            return Y, None, None

        y_opt, x_opt = optimize(evaluate, params_algo)
        print(f'best! {x_opt}: {y_opt}')
