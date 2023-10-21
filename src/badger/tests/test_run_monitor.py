import os


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
