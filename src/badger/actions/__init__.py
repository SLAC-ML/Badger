from pkg_resources import get_distribution
try:
    from ..factory import BADGER_PLUGIN_ROOT, BADGER_EXTENSIONS
except:
    BADGER_PLUGIN_ROOT = None
    BADGER_EXTENSIONS = None
try:
    from ..db import BADGER_DB_ROOT
except:
    BADGER_DB_ROOT = None
try:
    from ..logbook import BADGER_LOGBOOK_ROOT
except:
    BADGER_LOGBOOK_ROOT = None
try:
    from ..archive import BADGER_ARCHIVE_ROOT
except:
    BADGER_ARCHIVE_ROOT = None
from ..utils import yprint
from .doctor import check_n_config_paths


def show_info(args):
    if args.gui:
        from ..gui import launch_gui

        launch_gui()
    else:
        info = {
            'name': 'Badger the optimizer',
            'version': get_distribution('badger-opt').version,
            'plugin root': BADGER_PLUGIN_ROOT,
            'database root': BADGER_DB_ROOT,
            'logbook root': BADGER_LOGBOOK_ROOT,
            'archive root': BADGER_ARCHIVE_ROOT,
        }

        if BADGER_EXTENSIONS:
            extensions = list(BADGER_EXTENSIONS.keys())
            if extensions:
                info['extensions'] = extensions

        yprint(info)

        check_n_config_paths()
        # print(f'Badger the optimizer')
        # print('====================')
        # print(f'version      : {version}')
        # print(f'plugins root : {BADGER_PLUGIN_ROOT}')
