import os
from badger.tests.utils import create_routine


def test_init(qtbot):
    from badger.gui.default.components.routine_editor import BadgerRoutineEditor
    BadgerRoutineEditor()


def test_routine_set_and_save(qtbot):
    from badger.db import BADGER_DB_ROOT
    from badger.gui.default.components.routine_editor import BadgerRoutineEditor

    os.makedirs(BADGER_DB_ROOT, exist_ok=True)

    window = BadgerRoutineEditor()

    routine = create_routine()
    window.set_routine(routine)

    window.save_routine()
