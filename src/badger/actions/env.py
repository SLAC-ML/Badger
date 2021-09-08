from ..factory import list_env, get_env
from ..utils import yprint


def show_env(args):
    if args.env_name is None:
        yprint(list_env())
    else:
        yprint(get_env(args.env_name)[1])
