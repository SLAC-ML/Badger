from ..factory import list_algo, get_algo
from ..utils import yprint


def show_algo(args):
    if args.algo_name is None:
        yprint(list_algo())
        return

    algo = get_algo(args.algo_name)
    if algo is None:
        return
    yprint(algo[1])
