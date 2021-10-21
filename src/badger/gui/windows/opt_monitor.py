import numpy as np
from PyQt5.QtWidgets import QVBoxLayout, QHBoxLayout, QWidget, QPushButton, QMessageBox
from PyQt5.QtCore import pyqtSignal, QThreadPool
import pyqtgraph as pg
from ..components.routine_runner import BadgerRoutineRunner
# from ...utils import make_sync


class BadgerOptMonitor(QWidget):
    sig_pause = pyqtSignal(bool)  # True: pause, False: resume
    sig_stop = pyqtSignal()

    def __init__(self, parent, routine, save):
        super().__init__(parent)

        self.routine = routine
        self.save = save

        self.init_ui()
        self.config_logic()

    def init_ui(self):
        self.setWindowTitle('Opt Monitor')
        self.resize(1280, 640)

        vbox = QVBoxLayout(self)

        monitor = pg.GraphicsLayoutWidget()
        # monitor.resize(1000, 600)
        pg.setConfigOptions(antialias=True)

        self.plot_obj = plot_obj = monitor.addPlot(title='Evaluation History (Y)')
        plot_obj.setLabel('left', 'objectives')
        plot_obj.setLabel('bottom', 'iterations')
        plot_obj.showGrid(x=True, y=True)

        self.plot_var = plot_var = monitor.addPlot(title='Evaluation History (X)')
        plot_var.setLabel('left', 'variables')
        plot_var.setLabel('bottom', 'iterations')
        plot_var.showGrid(x=True, y=True)

        # Action bar
        action_bar = QWidget()
        hbox_action = QHBoxLayout(action_bar)
        hbox_action.setContentsMargins(0, 0, 0, 0)
        self.btn_ctrl = btn_ctrl = QPushButton('Pause')
        self.btn_stop = btn_stop = QPushButton('Stop')
        hbox_action.addStretch(1)
        hbox_action.addWidget(btn_ctrl)
        hbox_action.addWidget(btn_stop)

        vbox.addWidget(monitor)
        vbox.addWidget(action_bar)

    def config_logic(self):
        self.colors = ['b', 'g', 'r', 'c', 'm', 'y', 'w']
        self.symbols = ['o', 't', 't1', 's', 'p', 'h', 'd']
        self.vars = []
        self.objs = []
        self.curves_var = []
        self.curves_obj = []

        self.running = False

        # Thread runner
        self.thread_pool = QThreadPool(self)

        # Create the routine runner
        self.routine_runner = routine_runner = BadgerRoutineRunner(self.routine, self.save)
        routine_runner.signals.finished.connect(self.routine_finished)
        routine_runner.signals.progress.connect(self.update)

        self.sig_pause.connect(routine_runner.ctrl_routine)
        self.sig_stop.connect(routine_runner.stop_routine)

        self.btn_ctrl.clicked.connect(self.ctrl_routine)
        self.btn_stop.clicked.connect(self.stop_routine)

    def start(self):
        self.running = True  # if a routine runner is working
        self.thread_pool.start(self.routine_runner)

    def update(self, vars, objs):
        self.vars.append(vars)
        self.objs.append(objs)

        if not self.curves_obj:
            for i in range(len(objs)):
                color = self.colors[i % 7]
                symbol = self.symbols[i % 7]
                _curve = self.plot_obj.plot(pen=color, symbol=symbol)
                self.curves_obj.append(_curve)

        if not self.curves_var:
            for i in range(len(vars)):
                color = self.colors[i % 7]
                symbol = self.symbols[i % 7]
                _curve = self.plot_var.plot(pen=color, symbol=symbol)
                self.curves_var.append(_curve)

        for i in range(len(objs)):
            self.curves_obj[i].setData(np.array(self.objs)[:, i])

        for i in range(len(vars)):
            self.curves_var[i].setData(np.array(self.vars)[:, i])

    def routine_finished(self):
        self.running = False
        self.btn_ctrl.setDisabled(True)
        self.btn_stop.setDisabled(True)

    def ctrl_routine(self):
        if self.btn_ctrl.text() == 'Pause':
            self.sig_pause.emit(True)
            self.btn_ctrl.setText('Resume')
        else:
            self.sig_pause.emit(False)
            self.btn_ctrl.setText('Pause')

    def stop_routine(self):
        self.sig_stop.emit()

    def closeEvent(self, event):
        if not self.running:
            return

        reply = QMessageBox.question(self,
            'Window Close',
            'Closing this window will terminate the run, proceed?',
			QMessageBox.Yes | QMessageBox.No, QMessageBox.No)

        if reply == QMessageBox.Yes:
            self.sig_stop.emit()
            event.accept()
        else:
            event.ignore()
