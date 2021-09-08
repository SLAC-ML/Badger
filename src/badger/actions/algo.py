import yaml
from ..factory import list_algo, get_algo


def show_algo(args):
    if args.algo_name is None:
        print(yaml.dump(list_algo()))
    else:
        print(yaml.dump(get_algo(args.algo_name)[1]))
