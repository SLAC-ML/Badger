import logging
from ..factory import list_intf, get_intf
from ..utils import yprint


def show_intf(args):
    if args.intf_name is None:
        yprint(list_intf())
        return

    try:
        _, configs = get_intf(args.intf_name)
        yprint(configs)
    except Exception as e:
        logging.error(e)
        try:
            # The exception could carry the configs information
            configs = e.configs
            yprint(configs)
        except:
            pass
