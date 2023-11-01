import os
import sys
import time
from PyQt5.QtCore import Qt
from PyQt5.QtTest import QSignalSpy, QTest
from PyQt5.QtWidgets import QApplication, QMessageBox


def create_test_run_monitor():
    from badger.db import BADGER_DB_ROOT
    from badger.tests.utils import create_routine
    from badger.gui.default.components.run_monitor import BadgerOptMonitor

    os.makedirs(BADGER_DB_ROOT, exist_ok=True)

    monitor = BadgerOptMonitor()
    monitor.testing = True

    routine = create_routine()
    routine.random_evaluate(10)
    monitor.init_plots(routine)

    assert len(routine.data) == 10

    return monitor


def test_run_monitor(qtbot):
    from badger.db import BADGER_DB_ROOT
    from badger.tests.utils import create_routine
    from badger.gui.default.components.run_monitor import BadgerOptMonitor

    os.makedirs(BADGER_DB_ROOT, exist_ok=True)

    monitor = BadgerOptMonitor()
    monitor.testing = True
    qtbot.addWidget(monitor)

    routine = create_routine()

    # test initialization - first w/o routine
    monitor.init_plots()
    assert monitor.btn_stop.text() == 'Run'

    # test initialization - then w/ routine
    monitor.init_plots(routine)
    assert monitor.btn_stop.text() == 'Run'

    # add some data
    monitor.routine.step()
    assert len(monitor.routine.data) == 1

    # test updating plots
    monitor.update_curves()
    assert set(monitor.curves_variable.keys()) == {"x0", "x1", "x2", "x3"}
    assert set(monitor.curves_objective.keys()) == {"f"}
    assert set(monitor.curves_constraint.keys()) == {"c"}

    # set up run monitor and test it
    monitor.init_routine_runner()
    monitor.routine_runner.set_termination_condition(
        {"tc_idx": 0, "max_eval": 2}
    )
    spy = QSignalSpy(
        monitor.routine_runner.signals.progress
    )
    assert spy.isValid()
    QTest.mouseClick(monitor.btn_stop, Qt.MouseButton.LeftButton)
    time.sleep(1)
    QTest.mouseClick(monitor.btn_stop, Qt.MouseButton.LeftButton)


    # time.sleep(3)
    # qtbot.mouseClick(monitor.btn_stop, Qt.MouseButton.LeftButton)

    # assert monitor.var_names == ['x0', 'x1', 'x2', 'x3']


def test_routine_identity(qtbot):
    from badger.db import BADGER_DB_ROOT
    from badger.tests.utils import create_routine
    from badger.gui.default.components.run_monitor import BadgerOptMonitor

    os.makedirs(BADGER_DB_ROOT, exist_ok=True)

    monitor = BadgerOptMonitor()
    qtbot.addWidget(monitor)

    routine = create_routine()

    # Feed in the sample routine
    monitor.routine = routine
    monitor.init_routine_runner()

    assert monitor.routine_runner.routine == monitor.routine


def test_plotting(qtbot):
    monitor = create_test_run_monitor()
    monitor.update_curves()

    monitor.plot_x_axis = 1
    monitor.update_curves()

    monitor.plot_x_axis = 0
    monitor.x_plot_relative = 1
    monitor.update_curves()

    monitor.plot_x_axis = 1
    monitor.x_plot_relative = 1
    monitor.x_plot_y_axis = 1
    monitor.update_curves()


def test_click_graph(qtbot):
    monitor = create_test_run_monitor()
    QTest.mouseClick(monitor.btn_ctrl, Qt.MouseButton.LeftButton)

    raise NotImplementedError()


def test_x_axis_specification(qtbot):
    # check iteration/time drop down menu  
    monitor = create_test_run_monitor()    
    monitor.cb_plot_x.setCurrentIndex(0)
    # assert
    monitor.cb_plot_x.setCurrentIndex(1)
    # assert


def test_y_axis_specification(qtbot):
    monitor = create_test_run_monitor()

    # check raw - non relative 
    monitor.cb_plot_y.setCurrentIndex(0)
    # assert 

    # relative
    QTest.mouseClick(monitor.check_relative, Qt.MouseButton.LeftButton)
    # assert 

    # check if normalized relative
    monitor.cb_plot_y.setCurrentIndex(1)
    # assert

    # check normalized non relative. 
    QTest.mouseClick(monitor.check_relative, Qt.MouseButton.LeftButton)
    # assert


def test_pause_play(qtbot):
    monitor = create_test_run_monitor()
    spy = QSignalSpy(monitor.sig_pause)
    
    # 'click' the pause button. 
    QTest.mouseClick(monitor.btn_ctrl, Qt.MouseButton.LeftButton)
    assert spy.count() == 1
    # assert 
    
    QTest.mouseClick(monitor.btn_ctrl, Qt.MouseButton.LeftButton)
    assert spy.count() == 2
    # assert 


def test_jump_to_optimum(qtbot):
    monitor = create_test_run_monitor()
    spy = QSignalSpy(monitor.btn_opt.clicked)
    QTest.mouseClick(monitor.btn_opt, Qt.MouseButton.LeftButton)
    assert spy.count() == 1
    # check if it is going to optimal solution
    # assert


def test_reset_envrionment(qtbot):
    # check if reset button click signal is trigged and if state is same as original state after click 
    monitor = create_test_run_monitor()
    spy = QSignalSpy(monitor.btn_reset.clicked)

    QTest.mouseClick(monitor.btn_reset, Qt.MouseButton.LeftButton)
    assert spy.count() == 1
    # assert 


def test_dial_in_solution(qtbot):
    monitor = create_test_run_monitor()
    spy = QSignalSpy(monitor.btn_set.clicked)

    QTest.mouseClick(monitor.btn_set, Qt.MouseButton.LeftButton)
    assert spy.count() == 1
    # assert


def test_run_until(qtbot):
    monitor = create_test_run_monitor()
    QTest.mouseClick(monitor.btn_ctrl, Qt.MouseButton.LeftButton)

    raise NotImplementedError()


def test_add_extensions(qtbot):
    from badger.gui.default.components.run_monitor import BadgerOptMonitor
    from badger.gui.default.components.analysis_extensions import ParetoFrontViewer
    from badger.tests.utils import create_routine

    routine = create_routine()
    routine.vocs.objectives = {
        "f1": "MINIMIZE",
        "f2": "MAXIMIZE"
    }

    # test w/o using qtbot
    monitor = BadgerOptMonitor()
    monitor.routine = routine
    qtbot.addWidget(monitor)

    monitor.open_extensions_palette()
    monitor.extensions_palette.add_pf_viewer()

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
    assert monitor.extensions_palette.n_active_extensions == 0
