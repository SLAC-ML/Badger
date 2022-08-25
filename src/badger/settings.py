from PyQt5.QtCore import QSettings


BADGER_PATH_DICT = {
    'BADGER_PLUGIN_ROOT': {
        'display name': 'plugin root',
        'description': 'This setting (BADGER_PLUGIN_ROOT) tells Badger where to look for the plugins',
        'default value': None,
    },
    'BADGER_DB_ROOT': {
        'display name': 'database root',
        'description': 'This setting (BADGER_DB_ROOT) tells Badger where to store the routine database',
        'default value': None,
    },
    'BADGER_LOGBOOK_ROOT': {
        'display name': 'logbook root',
        'description': 'This setting (BADGER_LOGBOOK_ROOT) tells Badger where to send the logs (GUI mode)',
        'default value': None,
    },
    'BADGER_ARCHIVE_ROOT': {
        'display name': 'archive root',
        'description': 'This setting (BADGER_ARCHIVE_ROOT) tells Badger where to archive the historical optimization runs',
        'default value': None,
    },
}


BADGER_CORE_DICT = {
    'BADGER_CHECK_VAR_INTERVAL': {
        'display name': 'check var interval',
        'description': 'Waiting time between each round of check var when set var to env, unit is second',
        'default value': 0.1,
    },
    'BADGER_CHECK_VAR_TIMEOUT': {
        'display name': 'check var timeout',
        'description': 'Maximum waiting time before giving up check var if takes too long time, unit is second',
        'default value': 3,
    },
    'BADGER_PLUGINS_URL': {
        'display name': 'badger plugins url',
        'description': 'URL for badger plugins server',
        'default value': 'http://teeport.ml/badger-plugins'
    }
}


BADGER_GUI_DICT = {
    'BADGER_THEME': {
        'display name': 'theme',
        'description': 'Theme for the Badger GUI',
        'default value': 'dark',
    },
}


def init_settings():
    settings = QSettings('SLAC-ML', 'Badger')

    for key in BADGER_PATH_DICT.keys():
        if settings.value(key) is None:
            settings.setValue(key, BADGER_PATH_DICT[key]['default value'])
    for key in BADGER_CORE_DICT.keys():
        if settings.value(key) is None:
            settings.setValue(key, BADGER_CORE_DICT[key]['default value'])
    for key in BADGER_GUI_DICT.keys():
        if settings.value(key) is None:
            settings.setValue(key, BADGER_GUI_DICT[key]['default value'])


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
    for key in BADGER_CORE_DICT.keys():
        result[key] = settings.value(key)
    for key in BADGER_GUI_DICT.keys():
        result[key] = settings.value(key)

    return result


def read_value(key):
    settings = QSettings('SLAC-ML', 'Badger')

    return settings.value(key)


def write_value(key, value):
    settings = QSettings('SLAC-ML', 'Badger')

    settings.setValue(key, value)
