import logging
logger = logging.getLogger(__name__)
from ..utils import yprint


def show_algo(args):
    try:
        from ..factory import list_algo, get_algo
    except Exception as e:
        logger.error(e)
        return

    if args.algo_name is None:
        yprint(list_algo())
        return

    try:
        _, configs = get_algo(args.algo_name)
        yprint(configs)
    except Exception as e:
        logger.error(e)
        try:
            # The exception could carry the configs information
            configs = e.configs
            yprint(configs)
        except:
            pass
