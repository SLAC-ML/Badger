from ..factory import list_intf, get_intf
from ..utils import config_list_to_dict, yprint


def show_intf(args):
    if args.intf_name is None:
        yprint(list_intf())
        return

    intf, configs = get_intf(args.intf_name)
    if intf is None:
        return
    yprint(configs)
