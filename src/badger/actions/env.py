import yaml
from ..factory import list_env, get_env


def show_env(args):
    if args.env_name is None:
        print(yaml.dump(list_env()))
    else:
        print(yaml.dump(get_env(args.env_name)[1]))
