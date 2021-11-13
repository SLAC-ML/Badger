import os
import pytest


@pytest.fixture(scope='module', autouse=True)
def config_test_settings(request):
    from badger.settings import read_value, write_value

    # Store the old values
    old_root = read_value('BADGER_PLUGIN_ROOT')
    old_db = read_value('BADGER_DB_ROOT')
    old_logbook = read_value('BADGER_LOGBOOK_ROOT')
    old_archived = read_value('BADGER_ARCHIVE_ROOT')

    # Assign values for test
    test_root = os.path.join(request.fspath.dirname, 'plugins')
    test_db = os.path.join(request.fspath.dirname, 'db')
    test_logbook = os.path.join(request.fspath.dirname, 'logbook')
    test_archived = os.path.join(request.fspath.dirname, 'archived')

    write_value('BADGER_PLUGIN_ROOT', test_root)
    write_value('BADGER_DB_ROOT', test_db)
    write_value('BADGER_LOGBOOK_ROOT', test_logbook)
    write_value('BADGER_ARCHIVE_ROOT', test_archived)

    yield

    # Restoring the original settings
    write_value('BADGER_PLUGIN_ROOT', old_root)
    write_value('BADGER_DB_ROOT', old_db)
    write_value('BADGER_LOGBOOK_ROOT', old_logbook)
    write_value('BADGER_ARCHIVE_ROOT', old_archived)
