from PyQt5.QtCore import QSettings


def read_value(key):
    settings = QSettings('SLAC-ML', 'Badger')

    return settings.value(key)


def set_value(key, value):
    settings = QSettings('SLAC-ML', 'Badger')

    settings.setValue(key, value)
