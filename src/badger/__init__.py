import sys
import logging
try:
    from .factory import get_algo, get_intf, get_env
except Exception as e:  # TODO: add init setup guide!
    logging.error(e)
    sys.exit(-1)
