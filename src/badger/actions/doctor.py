import os
from ..settings import read_value, set_value


def self_check(args):
    good = check_n_config_paths()
    if good:
        print('Everything is fine!')


def _config_path_var(var_name, display_name):
    print(f'=== Configure {display_name} ===')
    while True:
        res = input(
            f'Please type in the path to the Badger {display_name} folder (S to skip): \n')
        if res == 'S':
            break

        res = os.path.abspath(os.path.expanduser(res))
        if os.path.isdir(res):
            _res = input(f'Your choice is {res}, proceed ([y]/n)? ')
            if _res == 'n':
                print('')
                continue
            elif (not _res) or (_res == 'y'):
                break
            else:
                print(f'Invalid choice: {_res}')
        else:
            _res = input(
                f'{res} does not exist, do you want to create it ([y]/n)? ')
            if _res == 'n':
                print('')
                continue
            elif (not _res) or (_res == 'y'):
                os.makedirs(res)
                print(f'Directory {res} has been created')
                break
            else:
                print(f'Invalid choice: {_res}')

    if res != 'S':
        set_value(var_name, res)
        print(f'You set the Badger {display_name} folder to {res}')


def check_n_config_paths():
    good = True

    if not read_value('BADGER_PLUGIN_ROOT'):
        good = False
        print('\nplugin root needs to be configured!\n')
        _config_path_var('BADGER_PLUGIN_ROOT', 'plugin root')

    if not read_value('BADGER_DB_ROOT'):
        good = False
        print('\ndatabase root needs to be configured!\n')
        _config_path_var('BADGER_DB_ROOT', 'database root')

    if not read_value('BADGER_LOGBOOK_ROOT'):
        good = False
        print('\nlogbook root needs to be configured!\n')
        _config_path_var('BADGER_LOGBOOK_ROOT', 'logbook root')

    if not read_value('BADGER_ARCHIVE_ROOT'):
        good = False
        print('\narchive root needs to be configured!\n')
        _config_path_var('BADGER_ARCHIVE_ROOT', 'archive root')

    return good
