from PyQt5.QtCore import QSettings


BADGER_PATH_DICT = {
    'BADGER_PLUGIN_ROOT': {'display name': 'plugin root'},
    'BADGER_DB_ROOT': {'display name': 'database root'},
    'BADGER_LOGBOOK_ROOT': {'display name': 'logbook root'},
    'BADGER_ARCHIVE_ROOT': {'display name': 'archive root'},
}


def list_settings():
    settings = QSettings('SLAC-ML', 'Badger')
    result = {}
    for key in BADGER_PATH_DICT.keys():
        result[key] = settings.value(key)

    return result


def read_value(key):
    settings = QSettings('SLAC-ML', 'Badger')

    return settings.value(key)


def set_value(key, value):
    settings = QSettings('SLAC-ML', 'Badger')

    settings.setValue(key, value)
