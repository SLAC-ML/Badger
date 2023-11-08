from PyQt5.QtCore import Qt


def test_gui_main(qtbot):
    from badger.gui.default.windows.main_window import BadgerMainWindow
    from badger.tests.utils import fix_db_path_issue

    fix_db_path_issue()

    window = BadgerMainWindow()
    qtbot.addWidget(window)

    # Test new routine feature
    qtbot.mouseClick(window.home_page.btn_new, Qt.MouseButton.LeftButton)
    assert window.stacks.currentWidget().tabs.currentIndex() == 1
