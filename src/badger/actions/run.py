import logging
logger = logging.getLogger(__name__)
from coolname import generate_slug
from ..utils import load_config, merge_params, normalize_routine
from ..utils import config_list_to_dict
from ..utils import run_routine as run


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
        # Normalize the routine configs properties
        try:
            _ = configs_routine['constraints']
        except KeyError:
            configs_routine['constraints'] = None
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

    try:
        run(routine, args.yes, args.save, args.verbose)
    except Exception as e:
        logger.error(e)
