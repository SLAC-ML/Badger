from PyQt5.QtCore import Qt


def test_gui_main(qtbot):
    from badger.gui.windows.main_window import BadgerMainWindow

    window = BadgerMainWindow()
    window.show()
    qtbot.addWidget(window)

    # Test new routine feature
    qtbot.mouseClick(window.home_page.btn_new, Qt.MouseButton.LeftButton)
    assert window.stacks.currentIndex() == 1
