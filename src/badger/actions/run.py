import numpy as np
from ..factory import get_algo, get_intf, get_env


def run_routine(args):
    Interface, configs_intf = get_intf('silly')
    Environment, configs_env = get_env('dumb')
    optimize, configs_algo = get_algo('silly')

    configs_routine = {
        'variables': ['q1', 'q3', 'q4', 's2'],
        'objectives': [{'l2_x_mean': 'MINIMIZE'}],
        'constraints': None,
    }

    params_algo = configs_algo['params'].copy()
    params_intf = configs_intf['params'].copy()
    params_env = None if not configs_env['params'] else configs_env['params'].copy()
    params_algo['dimension'] = len(configs_routine['variables'])
    params_algo['max_iter'] = 100
    params_intf['channel_prefix'] = 'c'
    params_intf['channel_count'] = 6

    intf = Interface(params_intf)
    env = Environment(intf, params_env)
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
