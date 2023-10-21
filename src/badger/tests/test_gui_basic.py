import os
from PyQt5.QtCore import Qt


def test_gui_main(qtbot):
    from badger.db import BADGER_DB_ROOT
    from badger.gui.default.windows.main_window import BadgerMainWindow

    os.makedirs(BADGER_DB_ROOT, exist_ok=True)

    window = BadgerMainWindow()
    qtbot.addWidget(window)

    # Test new routine feature
    qtbot.mouseClick(window.home_page.btn_new, Qt.MouseButton.LeftButton)
    assert window.stacks.currentWidget().tabs.currentIndex() == 1
