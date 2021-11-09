import logging
logger = logging.getLogger(__name__)
from ..factory import list_env, get_env
from ..utils import range_to_str, yprint


def show_env(args):
    if args.env_name is None:
        yprint(list_env())
        return

    try:
        _, configs = get_env(args.env_name)
    except Exception as e:
        logger.error(e)
        try:
            # The exception could carry the configs information
            configs = e.configs
        except:
            return

    try:
        configs['variables'] = range_to_str(configs['variables'])
        yprint(configs)
    except:
        pass
