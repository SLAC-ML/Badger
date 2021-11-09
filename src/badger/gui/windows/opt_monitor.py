import numpy as np
from PyQt5.QtWidgets import QVBoxLayout, QHBoxLayout, QWidget, QPushButton, QMessageBox
from PyQt5.QtCore import pyqtSignal, QThreadPool, Qt
from PyQt5.QtGui import QFont
import pyqtgraph as pg
from ..components.routine_runner import BadgerRoutineRunner
# from ..utils import AURORA_PALETTE, FROST_PALETTE
from ...logbook import send_to_logbook, BADGER_LOGBOOK_ROOT
from ...archive import archive_run, BADGER_ARCHIVE_ROOT


class BadgerOptMonitor(QWidget):
    sig_pause = pyqtSignal(bool)  # True: pause, False: resume
    sig_stop = pyqtSignal()

    def __init__(self, parent, routine, save):
        super().__init__()
        self._parent = parent  # used for aligning with the parent window
        self.setAttribute(Qt.WA_DeleteOnClose, True)

        self.routine = routine
        self.obj_names = [next(iter(d))
                          for d in self.routine['config']['objectives']]
        self.var_names = [next(iter(d))
                          for d in self.routine['config']['variables']]
        self.save = save

        self.init_ui()
        self.config_logic()

    def init_ui(self):
        self.setWindowTitle('Opt Monitor')
        self.resize(720, 960)
        self.center()

        vbox = QVBoxLayout(self)

        # Set up the monitor
        # Don't set show=True or there will be a blank window flashing once
        self.monitor = monitor = pg.GraphicsLayoutWidget()
        # monitor.ci.setBorder((50, 50, 100))
        # monitor.resize(1000, 600)
        pg.setConfigOptions(antialias=True)

        self.label = label = pg.LabelItem(justify='right')
        label.setText(self._make_label())
        monitor.addItem(label)

        monitor.nextRow()

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

        self.colors = ['c', 'g', 'm', 'y', 'b', 'r', 'w']
        self.symbols = ['o', 't', 't1', 's', 'p', 'h', 'd']
        self.curves_var = []
        self.curves_obj = []

        for i, obj_name in enumerate(self.obj_names):
            color = self.colors[i % len(self.colors)]
            symbol = self.symbols[i % len(self.colors)]
            _curve = self.plot_obj.plot(pen=pg.mkPen(color, width=3),
                                        # symbol=symbol,
                                        name=obj_name)
            self.curves_obj.append(_curve)

        for i, var_name in enumerate(self.var_names):
            color = self.colors[i % len(self.colors)]
            symbol = self.symbols[i % len(self.colors)]
            _curve = self.plot_var.plot(pen=pg.mkPen(color, width=3),
                                        # symbol=symbol,
                                        name=var_name)
            self.curves_var.append(_curve)

        self.ins_obj = pg.InfiniteLine(movable=True, angle=90, label=None,
                                       labelOpts={
                                           'position': 0.1,
                                           'color': (200, 200, 100),
                                           'fill': (200, 200, 200, 50),
                                           'movable': True})
        self.ins_var = pg.InfiniteLine(movable=True, angle=90, label=None,
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
        self.btn_log = btn_log = QPushButton('Logbook')
        btn_log.setFixedSize(64, 64)
        btn_log.setFont(cool_font)
        self.btn_reset = btn_reset = QPushButton('Reset')
        btn_reset.setDisabled(True)
        btn_reset.setFixedSize(64, 64)
        btn_reset.setFont(cool_font)
        self.btn_opt = btn_opt = QPushButton('Optimal')
        btn_opt.setFixedSize(64, 64)
        btn_opt.setFont(cool_font)
        self.btn_set = btn_set = QPushButton('Set')
        btn_set.setDisabled(True)
        btn_set.setFixedSize(64, 64)
        btn_set.setFont(cool_font)
        self.btn_ctrl = btn_ctrl = QPushButton('Pause')
        btn_ctrl.setFixedSize(64, 64)
        btn_ctrl.setFont(cool_font)
        self.btn_stop = btn_stop = QPushButton('Stop')
        btn_stop.setFixedSize(128, 64)
        btn_stop.setFont(cool_font)
        hbox_action.addWidget(btn_back)
        hbox_action.addStretch(1)
        hbox_action.addWidget(btn_log)
        hbox_action.addWidget(btn_reset)
        hbox_action.addWidget(btn_opt)
        hbox_action.addWidget(btn_set)
        hbox_action.addWidget(btn_ctrl)
        hbox_action.addWidget(btn_stop)

        vbox.addWidget(monitor)
        vbox.addWidget(action_bar)

    def config_logic(self):
        self.vars = []
        self.objs = []

        self.running = False

        # Sync the inspector lines
        self.ins_obj.sigDragged.connect(self.ins_obj_dragged)
        self.ins_obj.sigPositionChangeFinished.connect(self.ins_drag_done)
        self.ins_var.sigDragged.connect(self.ins_var_dragged)
        self.ins_var.sigPositionChangeFinished.connect(self.ins_drag_done)
        self.plot_obj.scene().sigMouseClicked.connect(self.on_mouse_click)
        # sigMouseReleased.connect(self.on_mouse_click)

        # Thread runner
        self.thread_pool = QThreadPool(self)

        # Create the routine runner
        self.routine_runner = routine_runner = BadgerRoutineRunner(
            self.routine, self.save)
        routine_runner.signals.env_ready.connect(self.env_ready)
        routine_runner.signals.finished.connect(self.routine_finished)
        routine_runner.signals.progress.connect(self.update)
        routine_runner.signals.error.connect(self.on_error)
        routine_runner.signals.info.connect(self.on_info)

        self.sig_pause.connect(routine_runner.ctrl_routine)
        self.sig_stop.connect(routine_runner.stop_routine)

        self.btn_back.clicked.connect(self.close)
        self.btn_log.clicked.connect(self.logbook)
        self.btn_reset.clicked.connect(self.reset_env)
        self.btn_opt.clicked.connect(self.jump_to_optimal)
        self.btn_set.clicked.connect(self.set_vars)
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

        for i in range(len(self.obj_names)):
            self.curves_obj[i].setData(np.array(self.objs)[:, i])

        for i in range(len(self.var_names)):
            self.curves_var[i].setData(np.array(self.vars)[:, i])

    def env_ready(self, init_vars):
        self.env = self.routine_runner.env
        self.init_vars = init_vars

    def routine_finished(self):
        self.running = False
        self.btn_ctrl.setDisabled(True)
        self.btn_stop.setDisabled(True)
        self.btn_reset.setDisabled(False)
        self.btn_set.setDisabled(False)
        try:
            archive_run(self.routine_runner.routine, self.routine_runner.data)
        except Exception as e:
            QMessageBox.critical(self, 'Archive failed!', str(e))

        QMessageBox.information(
            self, 'Success!', f'Run data archived to {BADGER_ARCHIVE_ROOT}')

    def on_error(self, error):
        QMessageBox.critical(self, 'Error!', str(error))

    def on_info(self, msg):
        QMessageBox.information(self, 'Info', msg)

    def logbook(self):
        try:
            send_to_logbook(None, self.monitor)
        except Exception as e:
            QMessageBox.critical(self, 'Log failed!', str(e))

        QMessageBox.information(
            self, 'Success!', f'Log saved to {BADGER_LOGBOOK_ROOT}')

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

    def ins_drag_done(self, ins):
        value = np.round(ins.value())
        self.ins_obj.setValue(value)
        self.ins_var.setValue(value)
        self.label.setText(self._make_label())

    def reset_env(self):
        current_vars = self.env.get_vars(self.var_names)
        self.env.set_vars(self.var_names, self.init_vars)
        after_vars = self.env.get_vars(self.var_names)
        QMessageBox.information(
            self, 'Reset Environment', f'Env vars {current_vars} -> {after_vars}')

    def jump_to_optimal(self):
        pf = self.routine_runner.pf
        idx = pf.pareto_set[0][0]
        self.ins_obj.setValue(idx)
        self.ins_var.setValue(idx)
        self.label.setText(self._make_label())

    def set_vars(self):
        df = self.routine_runner.data
        idx = int(self.ins_obj.value())
        solution = df.loc[idx, self.var_names].to_numpy()
        self.env.set_vars(self.var_names, solution)
        # center around the inspector
        self.plot_var.setXRange(idx - 3, idx + 3)
        # QMessageBox.information(
        #     self, 'Set Environment', f'Env vars have been set to {solution}')

    def _make_label(self):
        try:
            df = self.routine_runner.data
            idx = int(self.ins_obj.value())
            vars = df.loc[idx, self.var_names].to_numpy()
            objs = df.loc[idx, self.obj_names].to_numpy()
            var_label = ', '.join(
                [f'{var_name}: {vars[i]:.4f}' for i, var_name in enumerate(self.var_names)])
            obj_label = ', '.join(
                [f'{obj_name}: {objs[i]:.4f}' for i, obj_name in enumerate(self.obj_names)])
        except:
            var_label = ', '.join(
                [f'{var_name}: {np.nan:.4f}' for i, var_name in enumerate(self.var_names)])
            obj_label = ', '.join(
                [f'{obj_name}: {np.nan:.4f}' for i, obj_name in enumerate(self.obj_names)])

        return f"<span style='font-family: Courier; white-space: pre'>{var_label + ' | '}</span><span style='font-family: Courier; white-space: pre'>{obj_label}</span>"

    def on_mouse_click(self, event):
        # https://stackoverflow.com/a/64081483
        coor_obj = self.plot_obj.vb.mapSceneToView(event._scenePos)
        coor_var = self.plot_var.vb.mapSceneToView(event._scenePos)

        if self.plot_obj.viewRect().contains(coor_obj) or \
                self.plot_var.viewRect().contains(coor_var):
            idx = int(np.round(coor_obj.x()))

            self.ins_obj.setValue(idx)
            self.ins_var.setValue(idx)

            self.label.setText(self._make_label())

    def closeEvent(self, event):
        if not self.running:
            return

        reply = QMessageBox.question(self,
                                     'Window Close',
                                     'Closing this window will terminate the run, and the run data would NOT be archived! Proceed?',
                                     QMessageBox.Yes | QMessageBox.No, QMessageBox.No)

        if reply == QMessageBox.Yes:
            self.sig_stop.emit()
            event.accept()
        else:
            event.ignore()
