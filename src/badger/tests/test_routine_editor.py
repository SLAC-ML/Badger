import pandas as pd
import pytest
from PyQt5.QtCore import Qt

from badger.errors import BadgerRoutineError
from badger.tests.utils import create_routine


def test_init(qtbot):
    from badger.gui.default.components.routine_editor import BadgerRoutineEditor
    BadgerRoutineEditor()


def test_routine_set_and_save(qtbot):
    from badger.gui.default.components.routine_editor import BadgerRoutineEditor
    window = BadgerRoutineEditor()

    routine = create_routine()
    window.set_routine(routine)

    window.save_routine()


