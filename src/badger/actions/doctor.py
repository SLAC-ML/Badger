from ..settings import read_value, BADGER_PATH_DICT
from .config import _config_path_var


def self_check(args):
    good = check_n_config_paths()
    if good:
        print('Badger is healthy!')


def check_n_config_paths():
    good = True

    for pname in BADGER_PATH_DICT.keys():
        if not read_value(pname):
            good = False
            dname = BADGER_PATH_DICT[pname]['display name']
            print(f'\n{dname} needs to be configured!\n')

            try:
                _config_path_var(pname)
            except KeyboardInterrupt:
                pass

    return good
