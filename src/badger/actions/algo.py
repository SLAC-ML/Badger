from ..factory import list_algo, get_algo
from ..utils import config_list_to_dict, yprint


def show_algo(args):
    if args.algo_name is None:
        yprint(list_algo())
        return

    algo, configs = get_algo(args.algo_name)
    if algo is None:
        return
    yprint(configs)
