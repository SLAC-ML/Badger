from ..factory import list_intf, get_intf
from ..utils import yprint


def show_intf(args):
    if args.intf_name is None:
        yprint(list_intf())
        return

    intf = get_intf(args.intf_name)
    if intf is None:
        return
    yprint(intf[1])
