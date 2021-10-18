import sqlite3
from coolname import generate_slug
import logging
from ..factory import get_algo, get_env
from ..db import save_routine
from ..utils import load_config, merge_params


def run_test(args):
    Environment, configs_env = get_env(args.env)
    optimize, configs_algo = get_algo(args.algo)
    configs_routine = load_config(args.config)
    try:
        routine_name = configs_routine['name']
    except KeyError:
        routine_name = generate_slug(2)
        configs_routine['name'] = routine_name
    params_env = load_config(args.env_params)
    params_env = merge_params(configs_env['params'], params_env)
    params_algo = load_config(args.algo_params)
    params_algo = merge_params(configs_algo['params'], params_algo)

    # TODO: Sanity check here

    if not args.save:
        return

    routine = {
        'name': args.save,
        'algo': args.algo,
        'env': args.env,
        'algo_params': params_algo,
        'env_params': params_env,
        'config': configs_routine,
    }

    try:
        save_routine(routine)
    except sqlite3.IntegrityError:
        logging.error(f'Routine {args.save} already existed in the database! Please choose another name.')
