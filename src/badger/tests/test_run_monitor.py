import os
import sys
import time
from PyQt5.QtCore import Qt, QPoint
from PyQt5.QtTest import QSignalSpy, QTest
from PyQt5.QtWidgets import QApplication, QMessageBox, QMenu
from badger.tests.utils import create_routine
from badger.db import BADGER_DB_ROOT
from badger.gui.default.components.run_monitor import BadgerOptMonitor

def create_test_run_monitor():
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
    
    orginal_value = monitor.inspector_variable.value
    click_point = monitor.plot_obj.mapToGlobal(monitor.plot_obj.pos()) + QPoint(1, 0)
    qtbot.mouseClick(monitor.plot_obj, Qt.MouseButton.LeftButton, Qt.NoModifier, click_point)
    new_value = monitor.inspector_variable.value
    
    assert new_value != orginal_value
    assert new_value == 1 #hmmm


def test_x_axis_specification(qtbot):
    # check iteration/time drop down menu  
    monitor = create_test_run_monitor()    
    
    # read time stamp 
    # set inspector line index 1 

    # Iteration selected
    monitor.cb_plot_x.setCurrentIndex(0)
    
    # Test label setting 
    assert monitor.plot_var.label.textItem.text() == 'iterations'
    assert monitor.plot_obj.label.textItem.text() == 'iterations'
    if monitor.vocs.constraint_names:
        assert monitor.plot_con.label.textItem.text() == 'iterations'

    # Check if value is int 
    assert isinstance(monitor.inspector_objective.value, float)
    assert isinstance(monitor.inspector_variable.value, float)
    if monitor.vocs.constraint_names:
        assert isinstance(monitor.inspector_constraint.value, float)
    
    # Time selected 
    monitor.cb_plot_x.setCurrentIndex(1)
    
    # Test label setting
    assert monitor.plot_var.label.textItem.text() == 'time (s)'
    assert monitor.plot_obj.label.textItem.text() == 'time (s)'
    if monitor.vocs.constraint_names:
        assert monitor.plot_con.label.textItem.text() == 'time (s)'
    
    # Check if value is int 
    assert isinstance(monitor.inspector_objective.value, float)
    assert isinstance(monitor.inspector_variable.value, float)
    if monitor.vocs.constraint_names:
        assert isinstance(monitor.inspector_constraint.value, float)

def test_y_axis_specification(qtbot):
    monitor = create_test_run_monitor()

    # check raw - non relative 
    monitor.cb_plot_y.setCurrentIndex(0)
    # assert 

    # relative
    qtbot.mouseClick(monitor.check_relative, Qt.MouseButton.LeftButton)
    # assert 

    # check if normalized relative
    monitor.cb_plot_y.setCurrentIndex(1)
    # assert

    # check normalized non relative. 
    qtbot.mouseClick(monitor.check_relative, Qt.MouseButton.LeftButton)
    # assert


def test_pause_play(qtbot):
    monitor = create_test_run_monitor()
    spy = QSignalSpy(monitor.sig_pause)
    
    # 'click' the pause button. 
    qtbot.mouseClick(monitor.btn_ctrl, Qt.MouseButton.LeftButton)
    assert spy.count() == 1
    # assert 
    
    qtbot.mouseClick(monitor.btn_ctrl, Qt.MouseButton.LeftButton)
    assert spy.count() == 2
    # assert 


def test_jump_to_optimum(qtbot):
    monitor = create_test_run_monitor()
    spy = QSignalSpy(monitor.btn_opt.clicked)
    qtbot.mouseClick(monitor.btn_opt, Qt.MouseButton.LeftButton)
    assert spy.count() == 1
    # check if it is going to optimal solution
    # assert


def test_reset_envrionment(qtbot):
    # check if reset button click signal is trigged and if state is same as original state after click 
    monitor = create_test_run_monitor()
    spy = QSignalSpy(monitor.btn_reset.clicked)

    qtbot.mouseClick(monitor.btn_reset, Qt.MouseButton.LeftButton)
    assert spy.count() == 1
    # assert 


def test_dial_in_solution(qtbot):
    monitor = create_test_run_monitor()
    spy = QSignalSpy(monitor.btn_set.clicked)

    qtbot.mouseClick(monitor.btn_set, Qt.MouseButton.LeftButton)
    assert spy.count() == 1
    # assert


def test_run_until(qtbot):
    monitor = create_test_run_monitor()

    qtbot.mouseClick(monitor.btn_stop, Qt.MouseButton.LeftButton)
    menu = monitor.btn_stop.findChild(QMenu)
    qtbot.mouseClick(menu.actionGeometry(menu.actions()[1]).center(), Qt.LeftButton)
    
    # set max evaluation and then hit run in the pop up menu


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

