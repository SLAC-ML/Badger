import logging
logger = logging.getLogger(__name__)
import time
import pandas as pd
from coolname import generate_slug
from ..utils import load_config, merge_params
from ..utils import config_list_to_dict, curr_ts, ts_to_str
from ..core import run_routine as run
from ..core import normalize_routine


def run_n_archive(routine, yes=False, save=False, verbose=2,
                  fmt='lcls-log-full', sleep=0):
    try:
        from ..archive import archive_run
    except Exception as e:
        logger.error(e)
        return

    var_names = [next(iter(d)) for d in routine['config']['variables']]
    obj_names = [next(iter(d)) for d in routine['config']['objectives']]
    if routine['config']['constraints']:
        con_names = [next(iter(d)) for d in routine['config']['constraints']]
    else:
        con_names = []
    try:
        sta_names = routine['config']['states'] or []
    except KeyError:  # this would happen when rerun an old version routine
        sta_names = []
    # Store solutions in a list to avoid global var def
    solutions = []

    def after_evaluate(vars, obses, cons, stas):
        # vars: ndarray
        # obses: ndarray
        # cons: ndarray
        # stas: list
        ts = curr_ts()
        solution = [ts.timestamp(), ts_to_str(ts, fmt)] + list(obses) + list(cons) + list(vars) + stas
        solutions.append(solution)
        # take a break to let the outside signal to change the status
        time.sleep(sleep)
    # Store system states
    storage = {'states': None}
    def states_ready(states):
        storage['states'] = states

    try:
        run(routine, yes, save, verbose, after_evaluate=after_evaluate, states_ready=states_ready)
    except Exception as e:
        logger.error(e)

    if solutions:  # only save the run when at least one solution has been evaluated
        df = pd.DataFrame(solutions, columns=['timestamp_raw', 'timestamp'] + obj_names + con_names + var_names + sta_names)
        archive_run(routine, df, storage['states'])


def run_routine(args):
    try:
        from ..factory import get_algo, get_env
    except Exception as e:
        logger.error(e)
        return

    try:
        # Get env params
        _, configs_env = get_env(args.env)

        # Get algo params
        _, configs_algo = get_algo(args.algo)

        # Normalize the algo and env params
        params_env = load_config(args.env_params)
        params_algo = load_config(args.algo_params)
    except Exception as e:
        logger.error(e)
        return
    params_env = merge_params(configs_env['params'], params_env)
    params_algo = merge_params(configs_algo['params'], params_algo)

    # Load routine configs
    try:
        configs_routine = load_config(args.config)
    except Exception as e:
        logger.error(e)
        return

    # Compose the routine
    routine = {
        'name': args.save or generate_slug(2),
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
        logger.error(e)
        return

    run_n_archive(routine, args.yes, args.save, args.verbose)
