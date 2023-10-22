import os

from PyQt5.QtCore import Qt

from badger.gui.default.components.analysis_extensions import ParetoFrontViewer


def test_run_monitor(qtbot):
    from badger.db import BADGER_DB_ROOT
    from badger.tests.utils import create_routine
    from badger.gui.default.components.run_monitor import BadgerOptMonitor

    os.makedirs(BADGER_DB_ROOT, exist_ok=True)

    monitor = BadgerOptMonitor()
    monitor.show()
    qtbot.addWidget(monitor)

    routine = create_routine()

    # Feed in the sample routine
    # monitor.routine = routine
    # assert monitor.btn_stop.text() == 'Run'

    # qtbot.mouseClick(monitor.btn_stop, Qt.MouseButton.LeftButton)
    # time.sleep(3)
    # qtbot.mouseClick(monitor.btn_stop, Qt.MouseButton.LeftButton)
    # assert monitor.var_names == ['x0', 'x1', 'x2', 'x3']


def test_add_extensions(qtbot):
    from badger.gui.default.components.run_monitor import BadgerOptMonitor

    # test w/o using qtbot
    monitor = BadgerOptMonitor()
    monitor.show()
    qtbot.addWidget(monitor)

    monitor.open_extensions_palette()
    monitor.extensions_palette.add_data_viewer()

    assert isinstance(monitor.active_extensions[0], ParetoFrontViewer)

    # test opening and closing windows
    monitor = BadgerOptMonitor()
    qtbot.addWidget(monitor)

    qtbot.mouseClick(monitor.btn_open_extensions_palette, Qt.LeftButton)
    qtbot.mouseClick(monitor.extensions_palette.btn_data_viewer, Qt.LeftButton)
    assert isinstance(monitor.active_extensions[0], ParetoFrontViewer)
    assert len(monitor.active_extensions) == 1

    # test closing window -- should remove element from active extensions
    monitor.active_extensions[0].close()
    assert len(monitor.active_extensions) == 0
    assert monitor.extensions_palette.text_box.text() == "0"
