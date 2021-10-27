import numpy as np
from PyQt5.QtWidgets import QVBoxLayout, QHBoxLayout, QWidget, QPushButton, QMessageBox
from PyQt5.QtCore import pyqtSignal, QThreadPool, Qt
from PyQt5.QtGui import QFont
import pyqtgraph as pg
from ..components.routine_runner import BadgerRoutineRunner


class BadgerOptMonitor(QWidget):
    sig_pause = pyqtSignal(bool)  # True: pause, False: resume
    sig_stop = pyqtSignal()

    def __init__(self, parent, routine, save):
        super().__init__()
        self._parent = parent  # used for aligning with the parent window
        self.setAttribute(Qt.WA_DeleteOnClose, True)

        self.routine = routine
        self.save = save

        self.init_ui()
        self.config_logic()

    def init_ui(self):
        self.setWindowTitle('Opt Monitor')
        self.resize(640, 960)
        self.center()

        vbox = QVBoxLayout(self)

        # Set up the monitor
        # Don't set show=True or there will be a blank window flashing once
        self.monitor = monitor = pg.GraphicsLayoutWidget()
        # monitor.ci.setBorder((50, 50, 100))
        # monitor.resize(1000, 600)
        pg.setConfigOptions(antialias=True)

        self.plot_obj = plot_obj = monitor.addPlot(
            title='Evaluation History (Y)')
        plot_obj.setLabel('left', 'objectives')
        plot_obj.setLabel('bottom', 'iterations')
        plot_obj.showGrid(x=True, y=True)
        leg_obj = plot_obj.addLegend()
        leg_obj.setBrush((50, 50, 100, 200))

        monitor.nextRow()

        self.plot_var = plot_var = monitor.addPlot(
            title='Evaluation History (X)')
        plot_var.setLabel('left', 'variables')
        plot_var.setLabel('bottom', 'iterations')
        plot_var.showGrid(x=True, y=True)
        leg_var = plot_var.addLegend()
        leg_var.setBrush((50, 50, 100, 200))

        plot_var.setXLink(plot_obj)

        self.ins_obj = pg.InfiniteLine(movable=True, angle=90, label='x={value:0.2f}',
                                       labelOpts={
                                           'position': 0.1,
                                           'color': (200, 200, 100),
                                           'fill': (200, 200, 200, 50),
                                           'movable': True})
        self.ins_var = pg.InfiniteLine(movable=True, angle=90, label='x={value:0.2f}',
                                       labelOpts={
                                           'position': 0.1,
                                           'color': (200, 200, 100),
                                           'fill': (200, 200, 200, 50),
                                           'movable': True})
        plot_obj.addItem(self.ins_obj)
        plot_var.addItem(self.ins_var)

        # Action bar
        action_bar = QWidget()
        hbox_action = QHBoxLayout(action_bar)
        hbox_action.setContentsMargins(0, 0, 0, 0)

        cool_font = QFont()
        cool_font.setWeight(QFont.DemiBold)
        # cool_font.setPixelSize(16)

        self.btn_back = btn_back = QPushButton('Close')
        btn_back.setFixedSize(64, 64)
        btn_back.setFont(cool_font)
        self.btn_ctrl = btn_ctrl = QPushButton('Pause')
        btn_ctrl.setFixedSize(64, 64)
        btn_ctrl.setFont(cool_font)
        self.btn_stop = btn_stop = QPushButton('Stop')
        btn_stop.setFixedSize(128, 64)
        btn_stop.setFont(cool_font)
        hbox_action.addWidget(btn_back)
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

        # Sync the inspector lines
        self.ins_obj.sigDragged.connect(self.ins_obj_dragged)
        self.ins_var.sigDragged.connect(self.ins_var_dragged)

        # Thread runner
        self.thread_pool = QThreadPool(self)

        # Create the routine runner
        self.routine_runner = routine_runner = BadgerRoutineRunner(
            self.routine, self.save)
        routine_runner.signals.finished.connect(self.routine_finished)
        routine_runner.signals.progress.connect(self.update)
        routine_runner.signals.error.connect(self.on_error)

        self.sig_pause.connect(routine_runner.ctrl_routine)
        self.sig_stop.connect(routine_runner.stop_routine)

        self.btn_back.clicked.connect(self.close)
        self.btn_ctrl.clicked.connect(self.ctrl_routine)
        self.btn_stop.clicked.connect(self.stop_routine)

    def center(self):
        pass

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
                _curve = self.plot_obj.plot(pen=color, symbol=symbol,
                                            name=next(iter(self.routine['config']['objectives'][i])))
                self.curves_obj.append(_curve)

        if not self.curves_var:
            for i in range(len(vars)):
                color = self.colors[i % 7]
                symbol = self.symbols[i % 7]
                _curve = self.plot_var.plot(pen=color, symbol=symbol,
                                            name=next(iter(self.routine['config']['variables'][i])))
                self.curves_var.append(_curve)

        for i in range(len(objs)):
            self.curves_obj[i].setData(np.array(self.objs)[:, i])

        for i in range(len(vars)):
            self.curves_var[i].setData(np.array(self.vars)[:, i])

    def routine_finished(self):
        self.running = False
        self.btn_ctrl.setDisabled(True)
        self.btn_stop.setDisabled(True)

    def on_error(self, error):
         QMessageBox.critical(self, 'Error!', str(error))

    def ctrl_routine(self):
        if self.btn_ctrl.text() == 'Pause':
            self.sig_pause.emit(True)
            self.btn_ctrl.setText('Resume')
        else:
            self.sig_pause.emit(False)
            self.btn_ctrl.setText('Pause')

    def stop_routine(self):
        self.sig_stop.emit()

    def ins_obj_dragged(self, ins_obj):
        self.ins_var.setValue(ins_obj.value())

    def ins_var_dragged(self, ins_var):
        self.ins_obj.setValue(ins_var.value())

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
