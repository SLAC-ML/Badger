import numpy as np
from PyQt5.QtWidgets import QVBoxLayout, QHBoxLayout, QWidget, QPushButton, QCheckBox
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

stylesheet_log = '''
QPushButton:hover:pressed
{
    background-color: #5C8899;
}
QPushButton:hover
{
    background-color: #72A4B4;
}
QPushButton
{
    background-color: #88C0D0;
    color: #000000;
}
'''

stylesheet_run = '''
QPushButton:hover:pressed
{
    background-color: #92D38C;
}
QPushButton:hover
{
    background-color: #6EC566;
}
QPushButton
{
    background-color: #4AB640;
    color: #000000;
}
'''

stylesheet_stop = '''
QPushButton:hover:pressed
{
    background-color: #ed9c33;
}
QPushButton:hover
{
    background-color: #eb8f1a;
}
QPushButton
{
    background-color: #E98300;
    color: #000000;
}
'''


class BadgerOptMonitor(QWidget):
    sig_pause = pyqtSignal(bool)  # True: pause, False: resume
    sig_stop = pyqtSignal()
    sig_lock = pyqtSignal(bool)  # True: lock GUI, False: unlock GUI
    sig_new_run = pyqtSignal()
    sig_run_name = pyqtSignal(str)  # filename of the new run
    sig_inspect = pyqtSignal(int)  # index of the inspector
    sig_progress = pyqtSignal(list, list, list, list)  # new evaluated solution
    sig_del = pyqtSignal()

    def __init__(self):
        super().__init__()
        # self.setAttribute(Qt.WA_DeleteOnClose, True)

        # For plot type switching
        self.x_plot_y_axis = 0  # 0: raw, 1: normalized
        self.plot_x_axis = 0  # 0: iteration, 1: time
        self.x_plot_relative = True
        # Routine info
        self.routine = None
        self.var_names = []
        self.obj_names = []
        self.con_names = []
        self.sta_names = []
        self.vranges = []
        # Curves in the monitor
        self.curves_var = []
        self.curves_obj = []
        self.curves_con = []
        self.curves_sta = []
        # Data to be visualized
        self.vars = []
        self.objs = []
        self.cons = []
        self.stas = []
        self.ts = []
        # Run optimization
        self.thread_pool = None
        self.routine_runner = None
        self.running = False
        # Analysis tool for history runs
        self.pf = None
        # Fix the auto range issue
        self.eval_count = 0

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
        hbox_config.setContentsMargins(8, 0, 8, 0)
        label = QLabel('Evaluation History Plot Type')
        label_x = QLabel('X Axis')
        self.cb_plot_x = cb_plot_x = QComboBox()
        cb_plot_x.setItemDelegate(QStyledItemDelegate())
        cb_plot_x.addItems(['Iteration', 'Time'])
        label_y = QLabel('Y Axis (Var)')
        self.cb_plot_y = cb_plot_y = QComboBox()
        cb_plot_y.setItemDelegate(QStyledItemDelegate())
        cb_plot_y.addItems(['Raw', 'Normalized'])
        self.check_relative = check_relative = QCheckBox('Relative')
        check_relative.setChecked(True)
        hbox_config.addWidget(label)
        # hbox_config.addSpacing(1)
        hbox_config.addWidget(label_x)
        hbox_config.addWidget(cb_plot_x, 1)
        hbox_config.addWidget(label_y)
        hbox_config.addWidget(cb_plot_y, 1)
        hbox_config.addWidget(check_relative)

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
        monitor.nextRow()  # leave space for the stas plot
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
        self.ins_sta = pg.InfiniteLine(movable=True, angle=90, label=None,
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
        hbox_action.setContentsMargins(8, 0, 8, 0)

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
        btn_log.setFixedSize(128, 32)
        btn_log.setFont(cool_font)
        btn_log.setStyleSheet(stylesheet_log)
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
        btn_stop.setStyleSheet(stylesheet_run)
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
        self.ins_sta.sigDragged.connect(self.ins_sta_dragged)
        self.ins_sta.sigPositionChangeFinished.connect(self.ins_drag_done)
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
        self.cb_plot_x.currentIndexChanged.connect(self.select_x_axis)
        self.cb_plot_y.currentIndexChanged.connect(self.select_x_plot_y_axis)
        self.check_relative.stateChanged.connect(self.toggle_x_plot_y_axis_relative)

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
        try:
            self.sta_names = self.routine['config']['states'] or []
        except KeyError:  # this would happen when rerun an old version routine
            self.sta_names = []

        # Configure plots
        # Clear current plots
        self.plot_obj.clear()
        self.plot_obj.addItem(self.ins_obj)
        try:
            self.plot_con.clear()
            self.plot_con.addItem(self.ins_con)
        except:
            pass
        try:
            self.plot_sta.clear()
            self.plot_sta.addItem(self.ins_sta)
        except:
            pass
        self.plot_var.clear()
        self.plot_var.addItem(self.ins_var)
        # Put in the empty curves
        self.curves_var = []
        self.curves_obj = []
        self.curves_con = []
        self.curves_sta = []

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

        if self.sta_names:
            try:
                self.plot_sta
            except:
                self.plot_sta = plot_sta = self.monitor.addPlot(
                    row=2, col=0, title='Evaluation History (S)')
                plot_sta.setLabel('left', 'states')
                plot_sta.setLabel('bottom', 'iterations')
                plot_sta.showGrid(x=True, y=True)
                leg_sta = plot_sta.addLegend()
                leg_sta.setBrush((50, 50, 100, 200))
                plot_sta.addItem(self.ins_sta)
                plot_sta.setXLink(self.plot_obj)

            for i, sta_name in enumerate(self.sta_names):
                color = self.colors[i % len(self.colors)]
                symbol = self.symbols[i % len(self.colors)]
                _curve = self.plot_sta.plot(pen=pg.mkPen(color, width=3),
                                            # symbol=symbol,
                                            name=sta_name)
                self.curves_sta.append(_curve)
        else:
            try:
                self.monitor.removeItem(self.plot_sta)
                self.plot_sta.removeItem(self.ins_sta)
                del self.plot_sta
            except:
                pass

        # Reset inspectors
        self.ins_obj.setValue(0)
        self.ins_var.setValue(0)
        self.ins_con.setValue(0)
        self.ins_sta.setValue(0)

        # Switch run button state
        if self.routine:
            self.btn_stop.setDisabled(False)
        else:
            self.btn_stop.setDisabled(True)

        self.eval_count = 0  # reset the evaluation count
        self.enable_auto_range()

        # Fill in data
        self.data = data
        self.vars = []
        self.objs = []
        self.cons = []
        self.stas = []
        self.ts = []
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
        for sta in self.sta_names:
            self.stas.append(data[sta])
        self.stas = np.array(self.stas).T.tolist()
        self.ts = data['timestamp_raw']

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
        self.btn_stop.setStyleSheet(stylesheet_stop)
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
        if self.sta_names:
            self.plot_sta.enableAutoRange()

    def update_curves(self):
        type_x = self.plot_x_axis
        type_y = self.x_plot_y_axis
        relative = self.x_plot_relative

        if type_y:
            _vars = norm(np.array(self.vars),
                         self.vranges[:, 0], self.vranges[:, 1])
        else:
            _vars = np.array(self.vars)

        if relative:
            _vars = _vars - _vars[0]

        if type_x:
            ts = np.array(self.ts)
            ts -= ts[0]

        for i in range(len(self.var_names)):
            if type_x:
                self.curves_var[i].setData(ts, _vars[:, i])
            else:
                self.curves_var[i].setData(_vars[:, i])

        for i in range(len(self.obj_names)):
            if type_x:
                self.curves_obj[i].setData(ts, np.array(self.objs)[:, i])
            else:
                self.curves_obj[i].setData(np.array(self.objs)[:, i])

        if self.con_names:
            for i in range(len(self.con_names)):
                if type_x:
                    self.curves_con[i].setData(ts, np.array(self.cons)[:, i])
                else:
                    self.curves_con[i].setData(np.array(self.cons)[:, i])

        if self.sta_names:
            for i in range(len(self.sta_names)):
                if type_x:
                    self.curves_sta[i].setData(ts, np.array(self.stas)[:, i])
                else:
                    self.curves_sta[i].setData(np.array(self.stas)[:, i])

    def update(self, vars, objs, cons, stas, ts):
        self.vars.append(vars)
        self.objs.append(objs)
        self.cons.append(cons)
        self.stas.append(stas)
        self.ts.append(ts)

        self.update_curves()

        # Quick-n-dirty fix to the auto range issue
        self.eval_count += 1
        if self.eval_count < 5:
            self.enable_auto_range()

        self.sig_progress.emit(vars, objs, cons, stas)

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
        self.btn_stop.setStyleSheet(stylesheet_run)
        self.btn_reset.setDisabled(False)
        self.btn_set.setDisabled(False)
        self.btn_del.setDisabled(False)

        self.sig_lock.emit(False)

        try:
            run = archive_run(self.routine_runner.routine, self.routine_runner.data,
                self.routine_runner.states)
            self.routine_runner.run_filename = run['filename']
            self.sig_run_name.emit(run['filename'])

            QMessageBox.information(
                self, 'Success!', f'Archive succeeded: Run data archived to {BADGER_ARCHIVE_ROOT}')

        except Exception as e:
            self.sig_run_name.emit(None)

            QMessageBox.critical(self, 'Archive failed!', f'Archive failed: {str(e)}')

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
        if self.sta_names:
            self.ins_sta.setValue(ins_obj.value())

    def ins_con_dragged(self, ins_con):
        self.ins_var.setValue(ins_con.value())
        self.ins_obj.setValue(ins_con.value())
        if self.sta_names:
            self.ins_sta.setValue(ins_con.value())

    def ins_sta_dragged(self, ins_sta):
        self.ins_var.setValue(ins_sta.value())
        self.ins_obj.setValue(ins_sta.value())
        if self.con_names:
            self.ins_con.setValue(ins_sta.value())

    def ins_var_dragged(self, ins_var):
        self.ins_obj.setValue(ins_var.value())
        if self.con_names:
            self.ins_con.setValue(ins_var.value())
        if self.sta_names:
            self.ins_sta.setValue(ins_var.value())

    def ins_drag_done(self, ins):
        self.sync_ins(ins.value())

    def sync_ins(self, pos):
        if self.plot_x_axis:  # x-axis is time
            value, idx = self.closest_ts(pos)
        else:
            value = idx = np.clip(np.round(pos), 0, len(self.ts) - 1)
        self.ins_obj.setValue(value)
        if self.con_names:
            self.ins_con.setValue(value)
        if self.sta_names:
            self.ins_sta.setValue(value)
        self.ins_var.setValue(value)

        self.sig_inspect.emit(idx)

    def closest_ts(self, t):
        # Get the closest timestamp in self.ts regarding t
        ts = np.array(self.ts)
        ts -= ts[0]
        idx = np.argmin(np.abs(ts - t))

        return ts[idx], idx

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
        self.jump_to_solution(int(idx))
        self.sig_inspect.emit(idx)

    def jump_to_solution(self, idx):
        if self.plot_x_axis:  # x-axis is time
            value = self.ts[idx] -  self.ts[0]
        else:
            value = idx

        self.ins_obj.setValue(value)
        if self.con_names:
            self.ins_con.setValue(value)
        if self.sta_names:
            self.ins_sta.setValue(value)
        self.ins_var.setValue(value)

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

    def select_x_axis(self, i):
        self.plot_x_axis = i

        # Switch the x-axis labels
        if i:
            self.plot_var.setLabel('bottom', 'time (s)')
            self.plot_obj.setLabel('bottom', 'time (s)')
            if self.con_names:
                self.plot_con.setLabel('bottom', 'time (s)')
            if self.sta_names:
                self.plot_sta.setLabel('bottom', 'time (s)')
        else:
            self.plot_var.setLabel('bottom', 'iterations')
            self.plot_obj.setLabel('bottom', 'iterations')
            if self.con_names:
                self.plot_con.setLabel('bottom', 'iterations')
            if self.sta_names:
                self.plot_sta.setLabel('bottom', 'iterations')

        # Update inspector line position
        if i:
            value = self.ts[int(self.ins_obj.value())] - self.ts[0]
        else:
            _, value = self.closest_ts(self.ins_obj.value())
        self.ins_obj.setValue(value)
        if self.con_names:
            self.ins_con.setValue(value)
        if self.sta_names:
            self.ins_sta.setValue(value)
        self.ins_var.setValue(value)

        self.update_curves()
        self.enable_auto_range()

    def select_x_plot_y_axis(self, i):
        self.x_plot_y_axis = i
        self.update_curves()

    def toggle_x_plot_y_axis_relative(self):
        self.x_plot_relative = self.check_relative.isChecked()
        self.update_curves()

    def on_mouse_click(self, event):
        # https://stackoverflow.com/a/64081483
        coor_obj = self.plot_obj.vb.mapSceneToView(event._scenePos)
        if self.con_names:
            coor_con = self.plot_con.vb.mapSceneToView(event._scenePos)
        if self.sta_names:
            coor_sta = self.plot_sta.vb.mapSceneToView(event._scenePos)
        coor_var = self.plot_var.vb.mapSceneToView(event._scenePos)

        flag = self.plot_obj.viewRect().contains(coor_obj) or \
            self.plot_var.viewRect().contains(coor_var)
        if self.con_names:
            flag = flag or self.plot_con.viewRect().contains(coor_con)
        if self.sta_names:
            flag = flag or self.plot_sta.viewRect().contains(coor_sta)

        if flag:
            self.sync_ins(coor_obj.x())

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
