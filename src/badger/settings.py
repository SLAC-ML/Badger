from PyQt5.QtCore import QSettings


BADGER_PATH_DICT = {
    'BADGER_PLUGIN_ROOT': {
        'display name': 'plugin root',
        'description': 'This setting (BADGER_PLUGIN_ROOT) tells Badger where to look for the plugins',
    },
    'BADGER_DB_ROOT': {
        'display name': 'database root',
        'description': 'This setting (BADGER_DB_ROOT) tells Badger where to store the routine database',
    },
    'BADGER_LOGBOOK_ROOT': {
        'display name': 'logbook root',
        'description': 'This setting (BADGER_LOGBOOK_ROOT) tells Badger where to send the logs (GUI mode)',
    },
    'BADGER_ARCHIVE_ROOT': {
        'display name': 'archive root',
        'description': 'This setting (BADGER_ARCHIVE_ROOT) tells Badger where to archive the historical optimization runs',
    },
}


def list_settings():
    """List all the settings in Badger

    Returns
    -------
    dict
        A dictionary contains the settings. Keys in the dict are fields of the
        settings, the value for each key is the current value for that setting.

    """
    settings = QSettings('SLAC-ML', 'Badger')
    result = {}
    for key in BADGER_PATH_DICT.keys():
        result[key] = settings.value(key)

    return result


def read_value(key):
    settings = QSettings('SLAC-ML', 'Badger')

    return settings.value(key)


def write_value(key, value):
    settings = QSettings('SLAC-ML', 'Badger')

    settings.setValue(key, value)
