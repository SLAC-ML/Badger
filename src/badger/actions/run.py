import sqlite3
import numpy as np
import logging
# from coolname import generate_slug
from ..factory import get_algo, get_intf, get_env
from ..db import save_routine
from ..utils import load_config, yprint, merge_params, denorm, normalize_routine
from ..utils import config_list_to_dict, range_to_str, ParetoFront
from ..logger import _get_default_logger
from ..logger.event import Events


def run_routine(args):
    # Load env
    Environment, configs_env = get_env(args.env)
    try:
        intf_name = configs_env['interface'][0]
        Interface, _ = get_intf(intf_name)
        intf = Interface()
    except Exception:
        intf = None

    # Load algo
    optimize, configs_algo = get_algo(args.algo)
    # Normalize the algo and env params
    try:
        params_env = load_config(args.env_params)
        params_algo = load_config(args.algo_params)
    except Exception as e:
        logging.error(e)
        return
    params_env = merge_params(configs_env['params'], params_env)
    params_algo = merge_params(configs_algo['params'], params_algo)

    # Load routine configs
    try:
        configs_routine = load_config(args.config)
    except Exception as e:
        logging.error(e)
        return

    routine = {
        'name': args.save,
        'algo': args.algo,
        'env': args.env,
        'algo_params': params_algo,
        'env_params': params_env,
        # env_vranges is an additional info for the normalization
        # Will be removed after the normalization
        'env_vranges': config_list_to_dict(configs_env['variables']),
        'config': configs_routine,
    }
    # Sanity check and config normalization
    try:
        routine = normalize_routine(routine)
    except Exception as e:
        logging.error(e)
        return

    # Save routine if specified
    if args.save:
        try:
            save_routine(routine)
        except sqlite3.IntegrityError:
            logging.error(
                f'Routine {args.save} already existed in the database! Please choose another name.')
            return

    # Print out the routine info
    print('\n=== Optimization Routine ===')
    routine_configs_var = routine['config']['variables']
    routine['config']['variables'] = range_to_str(routine_configs_var)
    yprint(routine)
    print('')
    # TODO: Ask for user input if '-y' is not specified
    routine['config']['variables'] = routine_configs_var

    env = Environment(intf, params_env)

    if not callable(optimize):  # Doing optimization through extensions
        configs = {
            'routine_configs': routine['config'],
            'algo_configs': merge_params(configs_algo, {'params': params_algo})
        }
        results = optimize.run(env, configs)
        print('done!')
    else:
        # TODO: Make log level a CLI argument
        logger = _get_default_logger(2)  # log the optimization progress
        var_names = [next(iter(d)) for d in routine['config']['variables']]
        vranges = np.array([d[next(iter(d))] for d in routine['config']['variables']])
        obj_names = [next(iter(d)) for d in routine['config']['objectives']]
        rules = [d[next(iter(d))] for d in routine['config']['objectives']]
        pf = ParetoFront(rules)

        # Make a normalized evaluate function
        def evaluate(X):
            Y = []
            for x in X:
                _x = denorm(x, vranges[:, 0], vranges[:, 1])
                env.set_vars(var_names, _x)
                obses = []
                obses_raw = []
                for obj in configs_routine['objectives']:
                    key = list(obj.keys())[0]
                    ptype = list(obj.values())[0]
                    obs = env.get_obs(key)
                    if ptype == 'MAXIMIZE':
                        obses.append(-obs)
                    else:
                        obses.append(obs)
                    obses_raw.append(obs)
                Y.append(obses)
                obses_raw = np.array(obses_raw)
                is_optimal = not pf.is_dominated((_x, obses_raw))
                solution = (_x, obses_raw, is_optimal, var_names, obj_names)
                logger.update(Events.OPTIMIZATION_STEP, solution)

            Y = np.array(Y)

            return Y, None, None

        solution = (None, None, None, var_names, obj_names)
        logger.update(Events.OPTIMIZATION_START, solution)
        optimize(evaluate, params_algo)
        logger.update(Events.OPTIMIZATION_END, solution)
