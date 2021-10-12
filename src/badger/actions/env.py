from ..factory import list_env, get_env
from ..utils import range_to_str, yprint


def show_env(args):
    if args.env_name is None:
        yprint(list_env())
        return

    env, configs = get_env(args.env_name)
    if env is None:
        return

    configs['variables'] = range_to_str(configs['variables'])
    yprint(configs)
