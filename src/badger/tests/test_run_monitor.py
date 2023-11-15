import os
import sys
import time
from PyQt5.QtCore import Qt, QPoint, QPointF
from PyQt5.QtTest import QSignalSpy, QTest
from PyQt5.QtWidgets import QApplication, QMessageBox, QMenu
from PyQt5.QtGui import QMouseEvent
from badger.tests.utils import create_routine
from badger.db import BADGER_DB_ROOT
from badger.gui.default.components.run_monitor import BadgerOptMonitor
from unittest.mock import patch

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


def test_click_graph(qtbot, mocker):
    monitor = create_test_run_monitor()
    sig_inspect_spy = QSignalSpy(monitor.sig_inspect)
    monitor.plot_x_axis = True

    mock_event = mocker.MagicMock(spec=QMouseEvent)
    mock_event._scenePos = QPointF(350, 240)

    orginal_value = monitor.inspector_variable.value()
    monitor.on_mouse_click(mock_event)
    new_variable_value = monitor.inspector_variable.value()
    
    assert new_variable_value != orginal_value
    assert len(sig_inspect_spy) == 1


def test_x_axis_specification(qtbot):
    # check iteration/time drop down menu  
    monitor = create_test_run_monitor()    
    
    # read time stamp 
    time_value = monitor.inspector_variable.value()
    
    # set inspector line index 1 
    monitor.inspector_variable.setValue(1)

    # Iteration selected
    monitor.cb_plot_x.setCurrentIndex(0)
    
    # Test label setting 
    plot_var_axis = monitor.plot_var.getAxis('bottom')
    assert plot_var_axis.label.toPlainText().strip() == 'iterations'

    plot_obj_axis = monitor.plot_obj.getAxis('bottom')
    assert plot_obj_axis.label.toPlainText().strip() == 'iterations'

    if monitor.vocs.constraint_names:
        plot_con_axis = monitor.plot_con.getAxis('bottom')
        assert plot_con_axis.label.toPlainText().strip() == 'iterations'

    assert isinstance(monitor.inspector_objective.value(), int)
    assert isinstance(monitor.inspector_variable.value(), int)
    if monitor.vocs.constraint_names:
        assert isinstance(monitor.inspector_constraint.value(), int)
    
    # Time selected 
    monitor.cb_plot_x.setCurrentIndex(1)
    
    # Test label setting
    plot_var_axis_time = monitor.plot_var.getAxis('bottom')
    assert plot_var_axis_time.label.toPlainText().strip() == 'time (s)'

    plot_obj_axis_time = monitor.plot_obj.getAxis('bottom')
    assert plot_obj_axis_time.label.toPlainText().strip() == 'time (s)'

    if monitor.vocs.constraint_names:
        plot_con_axis_time = monitor.plot_con.getAxis('bottom')
        assert plot_con_axis_time.label.toPlainText().strip() == 'time (s)'
    
    # Check if value is int 
    assert isinstance(monitor.inspector_objective.value(), int)
    assert isinstance(monitor.inspector_variable.value(), float)
    if monitor.vocs.constraint_names:
        assert isinstance(monitor.inspector_constraint.value(), int)


def test_y_axis_specification(qtbot):
    monitor = create_test_run_monitor()
    select_x_plot_y_axis_spy = QSignalSpy(monitor.cb_plot_y.currentIndexChanged)

    # check raw - non relative 
    monitor.cb_plot_y.setCurrentIndex(0)
    assert len(select_x_plot_y_axis_spy) == 0 # since 0 is the default value

    # relative
    qtbot.mouseClick(monitor.check_relative, Qt.MouseButton.LeftButton)
    # assert 

    # check if normalized relative
    monitor.cb_plot_y.setCurrentIndex(1)
    assert len(select_x_plot_y_axis_spy) == 1

    # check normalized non relative. 
    qtbot.mouseClick(monitor.check_relative, Qt.MouseButton.LeftButton)
    # assert

'''
def test_pause_play(qtbot):
    monitor = create_test_run_monitor()
    spy = QSignalSpy(monitor.sig_pause)

    monitor.start(True)
    qtbot.wait(500)

    qtbot.mouseClick(monitor.btn_ctrl, Qt.MouseButton.LeftButton)
    assert len(spy) == 1
    
    qtbot.mouseClick(monitor.btn_ctrl, Qt.MouseButton.LeftButton)
    assert len(spy) == 2
    
    qtbot.mouseClick(monitor.btn_stop, Qt.MouseButton.LeftButton)
'''

def test_jump_to_optimum(qtbot):
    monitor = create_test_run_monitor()
    spy = QSignalSpy(monitor.btn_opt.clicked)
    orginal_value = monitor.inspector_variable.value()
    qtbot.mouseClick(monitor.btn_opt, Qt.MouseButton.LeftButton)

    qtbot.wait(500)

    optimal_value = monitor.inspector_variable.value()

    print(orginal_value, optimal_value)
    assert len(spy) == 1
    
    # check if it is going to optimal solution
    assert orginal_value != optimal_value


def test_reset_envrionment(qtbot):
    # check if reset button click signal is trigged and if state is same as original state after click 
    monitor = create_test_run_monitor()
    monitor.start(True)
    qtbot.wait(1000)
    spy = QSignalSpy(monitor.btn_reset.clicked)


    with patch('PyQt5.QtWidgets.QMessageBox.question', return_value=QMessageBox.Yes):
        with patch('PyQt5.QtWidgets.QMessageBox.information') as mock_info:
            monitor.reset_env()
            mock_info.assert_called_once()
            qtbot.mouseClick(monitor.btn_stop, Qt.MouseButton.LeftButton)


def test_dial_in_solution(qtbot):
    monitor = create_test_run_monitor()
    spy = QSignalSpy(monitor.btn_set.clicked)
    
    with patch('PyQt5.QtWidgets.QMessageBox.question', return_value=QMessageBox.Yes):
        qtbot.mouseClick(monitor.btn_set, Qt.MouseButton.LeftButton)
    
    assert len(spy) == 1

'''
def test_run_until(qtbot):
    monitor = create_test_run_monitor()
    monitor.run_until_action.trigger()

    # set max evaluation and then hit run in the pop up menu
'''

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

