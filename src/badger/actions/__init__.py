from pkg_resources import get_distribution
from ..factory import BADGER_PLUGIN_ROOT


def show_info(args):
    version = get_distribution('badger-opt').version
    print(f'Badger the optimizer')
    print('====================')
    print(f'version      : {version}')
    print(f'plugins root : {BADGER_PLUGIN_ROOT}')
