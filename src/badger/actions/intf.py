from ..factory import list_intf, get_intf
from ..utils import yprint


def show_intf(args):
    if args.intf_name is None:
        yprint(list_intf())
    else:
        yprint(get_intf(args.intf_name)[1])
