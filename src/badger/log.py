from logging.config import dictConfig
from .utils import merge_params


LOG_CONFIG_DEFAULT = {
    'version': 1,
    'formatters': {
        'simple': {
            'format': '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        }
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'level': 'DEBUG',
            'formatter': 'simple',
            'stream': 'ext://sys.stdout'
        }
    },
    'root': {
        'level': 'WARNING',
        'handlers': [
            'console'
        ]
    }
}


def config_log(dict_config=None):
    _config = merge_params(LOG_CONFIG_DEFAULT, dict_config)
    dictConfig(_config)
