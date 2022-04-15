import numpy as np
from PyQt5.QtWidgets import QVBoxLayout, QHBoxLayout, QWidget, QPushButton
from PyQt5.QtWidgets import QMessageBox, QComboBox, QLabel, QStyledItemDelegate
from PyQt5.QtCore import pyqtSignal, QThreadPool
from PyQt5.QtGui import QFont
import pyqtgraph as pg
from .routine_runner import BadgerRoutineRunner
# from ...utils import AURORA_PALETTE, FROST_PALETTE
from ...utils import norm, ParetoFront
from ...logbook import send_to_logbook, BADGER_LOGBOOK_ROOT
from ...archive import archive_run, BADGER_ARCHIVE_ROOT


stylesheet_del = '''
QPushButton:hover:pressed
{
    background-color: #C7737B;
}
QPushButton:hover
{
    background-color: #BF616A;
}
QPushButton
{
    background-color: #A9444E;
}
'''

class BadgerOptMonitor(QWidget):
    sig_pause = pyqtSignal(bool)  # True: pause, False: resume
    sig_stop = pyqtSignal()
    sig_lock = pyqtSignal(bool)  # True: lock GUI, False: unlock GUI
    sig_new_run = pyqtSignal()
    sig_run_name = pyqtSignal(str)  # filename of the new run
    sig_inspect = pyqtSignal(int)  # index of the inspector
    sig_progress = pyqtSignal(list, list, list)  # new evaluated solution
    sig_del = pyqtSignal()

    def __init__(self):
        super().__init__()
        # self.setAttribute(Qt.WA_DeleteOnClose, True)

        # For plot type switching
        self.x_plot_type = 0  # 0: raw, 1: normalized
        # Routine info
        self.routine = None
        self.var_names = []
        self.obj_names = []
        self.con_names = []
        self.vranges = []
        # Curves in the monitor
        self.curves_var = []
        self.curves_obj = []
        self.curves_con = []
        # Data to be visualized
        self.vars = []
        self.objs = []
        self.cons = []
        # Run optimization
        self.thread_pool = None
        self.routine_runner = None
        self.running = False
        # Analysis tool for history runs
        self.pf = None

        self.init_ui()
        self.config_logic()

    def init_ui(self):
        # self.main_panel = main_panel = QWidget(self)
        # main_panel.setStyleSheet('background-color: #19232D;')
        vbox = QVBoxLayout(self)
        vbox.setContentsMargins(0, 0, 0, 0)

        # Config bar
        config_bar = QWidget()
        hbox_config = QHBoxLayout(config_bar)
        hbox_config.setContentsMargins(0, 0, 0, 0)
        label = QLabel('Evaluation History (X) Plot Type')
        self.cb_plot = cb_plot = QComboBox()
        cb_plot.setItemDelegate(QStyledItemDelegate())
        cb_plot.addItems(['Raw', 'Normalized'])
        hbox_config.addWidget(label)
        hbox_config.addWidget(cb_plot, 1)

        # Set up the monitor
        # Don't set show=True or there will be a blank window flashing once
        self.monitor = monitor = pg.GraphicsLayoutWidget()
        pg.setConfigOptions(antialias=True)
        # monitor.ci.setBorder((50, 50, 100))
        # monitor.resize(1000, 600)

        self.plot_obj = plot_obj = monitor.addPlot(
            title='Evaluation History (Y)')
        plot_obj.setLabel('left', 'objectives')
        plot_obj.setLabel('bottom', 'iterations')
        plot_obj.showGrid(x=True, y=True)
        leg_obj = plot_obj.addLegend()
        leg_obj.setBrush((50, 50, 100, 200))

        monitor.nextRow()  # leave space for the cons plot
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

        self.ins_obj = pg.InfiniteLine(movable=True, angle=90, label=None,
                                       labelOpts={
                                           'position': 0.1,
                                           'color': (200, 200, 100),
                                           'fill': (200, 200, 200, 50),
                                           'movable': True})
        self.ins_con = pg.InfiniteLine(movable=True, angle=90, label=None,
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
        # action_bar.hide()
        hbox_action = QHBoxLayout(action_bar)
        hbox_action.setContentsMargins(0, 0, 0, 0)

        cool_font = QFont()
        cool_font.setWeight(QFont.DemiBold)
        # cool_font.setPixelSize(16)

        self.btn_del = btn_del = QPushButton('Delete Run')
        btn_del.setFixedSize(128, 32)
        btn_del.setFont(cool_font)
        btn_del.setStyleSheet(stylesheet_del)
        # self.btn_edit = btn_edit = QPushButton('Edit')
        # btn_edit.setFixedSize(64, 32)
        # btn_edit.setFont(cool_font)
        self.btn_log = btn_log = QPushButton('Logbook')
        btn_log.setFixedSize(64, 32)
        btn_log.setFont(cool_font)
        self.btn_reset = btn_reset = QPushButton('Reset')
        btn_reset.setDisabled(True)
        btn_reset.setFixedSize(64, 32)
        btn_reset.setFont(cool_font)
        self.btn_opt = btn_opt = QPushButton('Optimal')
        btn_opt.setFixedSize(64, 32)
        btn_opt.setFont(cool_font)
        self.btn_set = btn_set = QPushButton('Set')
        btn_set.setDisabled(True)
        btn_set.setFixedSize(64, 32)
        btn_set.setFont(cool_font)
        self.btn_ctrl = btn_ctrl = QPushButton('Pause')
        btn_ctrl.setDisabled(True)
        btn_ctrl.setFixedSize(64, 32)
        btn_ctrl.setFont(cool_font)
        self.btn_stop = btn_stop = QPushButton('Run')
        btn_stop.setDisabled(True)
        btn_stop.setFixedSize(128, 32)
        btn_stop.setFont(cool_font)
        hbox_action.addWidget(btn_del)
        # hbox_action.addWidget(btn_edit)
        hbox_action.addWidget(btn_log)
        hbox_action.addWidget(btn_opt)
        hbox_action.addStretch(1)
        hbox_action.addWidget(btn_reset)
        hbox_action.addWidget(btn_set)
        hbox_action.addWidget(btn_ctrl)
        hbox_action.addWidget(btn_stop)

        vbox.addWidget(config_bar)
        vbox.addWidget(monitor)
        vbox.addWidget(action_bar)

    def config_logic(self):
        # Sync the inspector lines
        self.ins_obj.sigDragged.connect(self.ins_obj_dragged)
        self.ins_obj.sigPositionChangeFinished.connect(self.ins_drag_done)
        self.ins_con.sigDragged.connect(self.ins_con_dragged)
        self.ins_con.sigPositionChangeFinished.connect(self.ins_drag_done)
        self.ins_var.sigDragged.connect(self.ins_var_dragged)
        self.ins_var.sigPositionChangeFinished.connect(self.ins_drag_done)
        self.plot_obj.scene().sigMouseClicked.connect(self.on_mouse_click)
        # sigMouseReleased.connect(self.on_mouse_click)

        # Thread runner
        self.thread_pool = QThreadPool(self)

        self.btn_del.clicked.connect(self.delete_run)
        self.btn_log.clicked.connect(self.logbook)
        self.btn_reset.clicked.connect(self.reset_env)
        self.btn_opt.clicked.connect(self.jump_to_optimal)
        self.btn_set.clicked.connect(self.set_vars)
        self.btn_ctrl.clicked.connect(self.ctrl_routine)
        self.btn_stop.clicked.connect(self.run_stop_routine)

        # Visualization
        self.cb_plot.currentIndexChanged.connect(self.select_x_plot_type)

    def init_plots(self, routine, data=None, run_filename=None):
        # Parse routine
        self.routine = routine
        try:
            self.obj_names = [next(iter(d))
                              for d in self.routine['config']['objectives']]
        except:
            self.obj_names = []
        try:
            self.var_names = [next(iter(d))
                              for d in self.routine['config']['variables']]
        except:
            self.var_names = []
        try:
            self.vranges = np.array([d[next(iter(d))]
                                    for d in routine['config']['variables']])
        except:
            self.vranges = []
        try:
            if self.routine['config']['constraints']:
                self.con_names = [next(iter(d))
                                  for d in self.routine['config']['constraints']]
            else:
                self.con_names = []
        except:
            self.con_names = []

        # Configure plots
        # Clear current plots
        self.plot_obj.clear()
        self.plot_obj.addItem(self.ins_obj)
        try:
            self.plot_con.clear()
            self.plot_con.addItem(self.ins_con)
        except:
            pass
        self.plot_var.clear()
        self.plot_var.addItem(self.ins_var)
        # Put in the empty curves
        self.curves_var = []
        self.curves_obj = []
        self.curves_con = []

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

        if self.con_names:
            try:
                self.plot_con
            except:
                self.plot_con = plot_con = self.monitor.addPlot(
                    row=1, col=0, title='Evaluation History (C)')
                plot_con.setLabel('left', 'constraints')
                plot_con.setLabel('bottom', 'iterations')
                plot_con.showGrid(x=True, y=True)
                leg_con = plot_con.addLegend()
                leg_con.setBrush((50, 50, 100, 200))
                plot_con.addItem(self.ins_con)
                plot_con.setXLink(self.plot_obj)

            for i, con_name in enumerate(self.con_names):
                color = self.colors[i % len(self.colors)]
                symbol = self.symbols[i % len(self.colors)]
                _curve = self.plot_con.plot(pen=pg.mkPen(color, width=3),
                                            # symbol=symbol,
                                            name=con_name)
                self.curves_con.append(_curve)
        else:
            try:
                self.monitor.removeItem(self.plot_con)
                self.plot_con.removeItem(self.ins_con)
                del self.plot_con
            except:
                pass
        # Reset inspectors
        self.ins_obj.setValue(0)
        self.ins_var.setValue(0)
        self.ins_con.setValue(0)

        # Switch run button state
        if self.routine:
            self.btn_stop.setDisabled(False)
        else:
            self.btn_stop.setDisabled(True)

        # Fill in data
        self.data = data
        self.vars = []
        self.objs = []
        self.cons = []
        if self.routine_runner and self.routine_runner.run_filename == run_filename:
            self.btn_reset.setDisabled(False)
            self.btn_set.setDisabled(False)
        else:
            self.btn_reset.setDisabled(True)
            self.btn_set.setDisabled(True)
        if data is None:
            self.btn_del.setDisabled(True)
            self.btn_log.setDisabled(True)
            self.btn_opt.setDisabled(True)
            self.enable_auto_range()
            return

        for var in self.var_names:
            self.vars.append(data[var])
        self.vars = np.array(self.vars).T.tolist()
        for obj in self.obj_names:
            self.objs.append(data[obj])
        self.objs = np.array(self.objs).T.tolist()
        for con in self.con_names:
            self.cons.append(data[con])
        self.cons = np.array(self.cons).T.tolist()

        self.update_curves()

        self.calc_optimals()
        self.btn_del.setDisabled(False)
        self.btn_log.setDisabled(False)
        self.btn_opt.setDisabled(False)

    def init_routine_runner(self):
        self.reset_routine_runner()

        self.routine_runner = routine_runner = BadgerRoutineRunner(
            self.routine, False)
        routine_runner.signals.env_ready.connect(self.env_ready)
        routine_runner.signals.finished.connect(self.routine_finished)
        routine_runner.signals.progress.connect(self.update)
        routine_runner.signals.error.connect(self.on_error)
        routine_runner.signals.info.connect(self.on_info)

        self.sig_pause.connect(routine_runner.ctrl_routine)
        self.sig_stop.connect(routine_runner.stop_routine)

    def reset_routine_runner(self):
        if self.routine_runner:
            self.sig_pause.disconnect()
            self.sig_stop.disconnect()
            self.routine_runner = None

    def calc_optimals(self):
        rules = [d[next(iter(d))] for d in self.routine['config']['objectives']]
        self.pf = pf = ParetoFront(rules)

        for i, v in enumerate(self.vars):
            o = self.objs[i]
            idx = [i,] + v
            pf.is_dominated((idx, o))

    def start(self):
        self.sig_new_run.emit()
        self.init_plots(self.routine)
        self.init_routine_runner()
        self.running = True  # if a routine runner is working
        self.thread_pool.start(self.routine_runner)

        self.btn_stop.setText('Stop')
        self.btn_ctrl.setDisabled(False)
        self.sig_lock.emit(True)

    def is_critical(self, cons):
        if not self.con_names:
            return False, None

        constraints = self.routine['config']['constraints']
        for i, con_dict in enumerate(constraints):
            name = self.con_names[i]
            if len(con_dict[name]) != 3:
                continue

            value = cons[i]
            relation, thres = con_dict[name][:2]
            if relation == 'GREATER_THAN':
                if value <= thres:
                    return True, f'{name} (current value: {value:.4f}) is less than {thres}!'
            elif relation == 'LESS_THAN':
                if value >= thres:
                    return True, f'{name} (current value: {value:.4f}) is greater than {thres}!'
            else:
                if value != thres:
                    return True, f'{name} (current value: {value:.4f}) is not equal to {thres}!'

        return False, None

    def enable_auto_range(self):
        # Enable autorange
        self.plot_obj.enableAutoRange()
        self.plot_var.enableAutoRange()
        if self.con_names:
            self.plot_con.enableAutoRange()

    def update_curves(self):
        for i in range(len(self.obj_names)):
            self.curves_obj[i].setData(np.array(self.objs)[:, i])

        if self.con_names:
            for i in range(len(self.con_names)):
                self.curves_con[i].setData(np.array(self.cons)[:, i])

        if self.x_plot_type:
            _vars = norm(np.array(self.vars),
                         self.vranges[:, 0], self.vranges[:, 1])
        else:
            _vars = np.array(self.vars)
        for i in range(len(self.var_names)):
            self.curves_var[i].setData(_vars[:, i])

        self.enable_auto_range()

    def update(self, vars, objs, cons):
        self.vars.append(vars)
        self.objs.append(objs)
        self.cons.append(cons)

        self.update_curves()
        self.sig_progress.emit(vars, objs, cons)

        # Check critical condition
        critical, msg = self.is_critical(cons)
        if not critical:
            return

        self.sig_pause.emit(True)
        self.btn_ctrl.setText('Resume')

        reply = QMessageBox.warning(self,
                                    'Run Paused',
                                    f'Critical constraint was violated: {msg}\nTerminate the run?',
                                    QMessageBox.Yes | QMessageBox.No, QMessageBox.Yes)
        if reply == QMessageBox.Yes:
            self.sig_stop.emit()

    def env_ready(self, init_vars):
        self.env = self.routine_runner.env
        self.init_vars = init_vars

        self.btn_log.setDisabled(False)
        self.btn_opt.setDisabled(False)

    def routine_finished(self):
        self.running = False
        self.btn_ctrl.setText('Pause')
        self.btn_ctrl.setDisabled(True)
        self.btn_stop.setText('Run')
        self.btn_reset.setDisabled(False)
        self.btn_set.setDisabled(False)
        self.btn_del.setDisabled(False)

        self.sig_lock.emit(False)

        try:
            run = archive_run(self.routine_runner.routine, self.routine_runner.data)
            self.routine_runner.run_filename = run['filename']
            self.sig_run_name.emit(run['filename'])
        except Exception as e:
            QMessageBox.critical(self, 'Archive failed!', str(e))

        QMessageBox.information(
            self, 'Success!', f'Run data archived to {BADGER_ARCHIVE_ROOT}')

    def on_error(self, error):
        QMessageBox.critical(self, 'Error!', str(error))

    # Do not show info -- too distracting
    def on_info(self, msg):
        pass
        # QMessageBox.information(self, 'Info', msg)

    def logbook(self):
        try:
            if self.routine_runner:
                routine = self.routine_runner.routine
                data = self.routine_runner.data.to_dict('list')
            else:
                routine = self.routine
                data = self.data
            send_to_logbook(routine, data, self.monitor)
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

    def run_stop_routine(self):
        if self.btn_stop.text() == 'Run':
            self.start()
        else:
            self.sig_stop.emit()

    def ins_obj_dragged(self, ins_obj):
        self.ins_var.setValue(ins_obj.value())
        if self.con_names:
            self.ins_con.setValue(ins_obj.value())

    def ins_con_dragged(self, ins_con):
        self.ins_var.setValue(ins_con.value())
        self.ins_obj.setValue(ins_con.value())

    def ins_var_dragged(self, ins_var):
        self.ins_obj.setValue(ins_var.value())
        if self.con_names:
            self.ins_con.setValue(ins_var.value())

    def ins_drag_done(self, ins):
        value = np.round(ins.value())
        self.ins_obj.setValue(value)
        if self.con_names:
            self.ins_con.setValue(value)
        self.ins_var.setValue(value)

        self.sig_inspect.emit(value)

    def reset_env(self):
        reply = QMessageBox.question(self,
                                     'Reset Environment',
                                     f'Are you sure you want to reset the env vars back to {self.init_vars}?',
                                     QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply != QMessageBox.Yes:
            return

        current_vars = self.env._get_vars(self.var_names)
        self.env._set_vars(self.var_names, self.init_vars)
        after_vars = self.env._get_vars(self.var_names)
        QMessageBox.information(
            self, 'Reset Environment', f'Env vars {current_vars} -> {after_vars}')

    def jump_to_optimal(self):
        try:
            pf = self.pf
        except:
            pf = self.routine_runner.pf
        if pf is None:
            return

        idx = pf.pareto_set[0][0]
        self.ins_obj.setValue(idx)
        if self.con_names:
            self.ins_con.setValue(idx)
        self.ins_var.setValue(idx)

        self.sig_inspect.emit(idx)

    def jump_to_solution(self, idx):
        self.ins_obj.setValue(idx)
        if self.con_names:
            self.ins_con.setValue(idx)
        self.ins_var.setValue(idx)

    def set_vars(self):
        df = self.routine_runner.data
        idx = int(self.ins_obj.value())
        solution = df.loc[idx, self.var_names].to_numpy()

        reply = QMessageBox.question(self,
                                     'Apply Solution',
                                     f'Are you sure you want to apply the current solution at {solution} to env?',
                                     QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply != QMessageBox.Yes:
            return

        self.env._set_vars(self.var_names, solution)
        # center around the inspector
        self.plot_var.setXRange(idx - 3, idx + 3)
        # QMessageBox.information(
        #     self, 'Set Environment', f'Env vars have been set to {solution}')

    def select_x_plot_type(self, i):
        self.x_plot_type = i
        if i:
            _vars = norm(np.array(self.vars),
                         self.vranges[:, 0], self.vranges[:, 1])
        else:
            _vars = np.array(self.vars)
        for i in range(len(self.var_names)):
            self.curves_var[i].setData(_vars[:, i])

    def on_mouse_click(self, event):
        # https://stackoverflow.com/a/64081483
        coor_obj = self.plot_obj.vb.mapSceneToView(event._scenePos)
        if self.con_names:
            coor_con = self.plot_con.vb.mapSceneToView(event._scenePos)
        coor_var = self.plot_var.vb.mapSceneToView(event._scenePos)

        flag = self.plot_obj.viewRect().contains(coor_obj) or \
            self.plot_var.viewRect().contains(coor_var)
        if self.con_names:
            flag = flag or self.plot_con.viewRect().contains(coor_con)

        if flag:
            idx = int(np.round(coor_obj.x()))

            self.ins_obj.setValue(idx)
            if self.con_names:
                self.ins_con.setValue(idx)
            self.ins_var.setValue(idx)

            self.sig_inspect.emit(idx)

    def delete_run(self):
        self.sig_del.emit()

    # def closeEvent(self, event):
    #     if not self.running:
    #         return

    #     reply = QMessageBox.question(self,
    #                                  'Window Close',
    #                                  'Closing this window will terminate the run, and the run data would NOT be archived! Proceed?',
    #                                  QMessageBox.Yes | QMessageBox.No, QMessageBox.No)

    #     if reply == QMessageBox.Yes:
    #         self.sig_stop.emit()
    #         event.accept()
    #     else:
    #         event.ignore()
