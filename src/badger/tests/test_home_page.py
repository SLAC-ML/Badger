

import pandas as pd
import pytest
from PyQt5.QtCore import Qt

from badger.errors import BadgerRoutineError


def test_home_page_init(qtbot):
    from badger.gui.default.pages.home_page import BadgerHomePage

    window = BadgerHomePage()

    qtbot.addWidget(window)


def test_homepage_select_routine(qtbot):
    from badger.gui.default.pages.home_page import BadgerHomePage

    window = BadgerHomePage()

    qtbot.addWidget(window)
