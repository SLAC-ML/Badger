from ..factory import list_algo, get_algo
from ..utils import yprint


def show_algo(args):
    if args.algo_name is None:
        yprint(list_algo())
    else:
        yprint(get_algo(args.algo_name)[1])
