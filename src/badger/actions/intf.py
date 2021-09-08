import yaml
from ..factory import list_intf, get_intf


def show_intf(args):
    if args.intf_name is None:
        print(yaml.dump(list_intf()))
    else:
        print(yaml.dump(get_intf(args.intf_name)[1]))
