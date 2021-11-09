import sys
from .log import config_log
config_log()
import logging
logger = logging.getLogger(__name__)
try:
    from .factory import get_algo, get_intf, get_env
except Exception as e:  # TODO: add init setup guide!
    logger.error(e)
    sys.exit(-1)
