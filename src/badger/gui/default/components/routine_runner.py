import logging
logger = logging.getLogger(__name__)
import os
import time
import pandas as pd
from pandas import DataFrame
from PyQt5.QtCore import pyqtSignal, QObject, QRunnable
from ....utils import curr_ts, ts_to_str
from ....core import run_routine, Routine
from ....settings import read_value
from ....archive import archive_run
from ....errors import BadgerRunTerminatedError


class BadgerRoutineSignals(QObject):
    env_ready = pyqtSignal(list)
    finished = pyqtSignal()
    progress = pyqtSignal(list, list, list, list, float)
    error = pyqtSignal(Exception)
    info = pyqtSignal(str)


class BadgerRoutineRunner(QRunnable):

    def __init__(self, routine: Routine, save, verbose=2, use_full_ts=False):
        super().__init__()

        # Signals should belong to instance rather than class
        # Since there could be multiple runners runing in parallel
        self.signals = BadgerRoutineSignals()

        self.routine = routine
        self.run_filename = None
        self.states = None  # system states to be saved at start of a run
        self.save = save
        self.verbose = verbose
        self.use_full_ts = use_full_ts
        self.termination_condition = None  # additional option to control the optimization flow
        self.start_time = None  # track the time cost of the run
        self.last_dump_time = None  # track the time the run data got dumped

        self.is_paused = False
        self.is_killed = False

    def set_termination_condition(self, termination_condition):
        self.termination_condition = termination_condition

    def run(self):
        self.start_time = time.time()
        self.last_dump_time = None  # reset the timer

        try:
            run_routine(
                self.routine,
                active_callback=self.run_status,
                generate_callback=self.before_evaluate_xopt,
                evaluate_callback=self.after_evaluate_xopt,
                states_callback=self.states_ready
            )
        except BadgerRunTerminatedError as e:
            self.signals.finished.emit()
            self.signals.info.emit(str(e))
        except Exception as e:
            logger.exception(e)
            self.signals.finished.emit()
            self.signals.error.emit(e)

    def before_evaluate(self, vars):
        # vars: ndarray
        while self.is_paused:
            time.sleep(0)
            if self.is_killed:
                raise BadgerRunTerminatedError

        if self.is_killed:
            raise BadgerRunTerminatedError

    def after_evaluate(self, vars, obses, cons, stas):
        # vars: ndarray
        # obses: ndarray
        # cons: ndarray
        # stas: list
        ts = curr_ts()
        ts_float = ts.timestamp()
        self.signals.progress.emit(list(vars), list(obses), list(cons), list(stas), ts_float)

        # Append solution to data
        fmt = 'lcls-log-full' if self.use_full_ts else 'lcls-log'
        solution = [ts.timestamp(), ts_to_str(ts, fmt)] + list(obses) + list(cons) + list(vars) + list(stas)
        new_row = pd.Series(solution, index=self.data.columns)
        self.data = pd.concat([self.data, new_row.to_frame().T], ignore_index=True)

        # Try dump the run data and interface log to the disk
        dump_period = float(read_value('BADGER_DATA_DUMP_PERIOD'))
        if (self.last_dump_time is None) or (ts_float - self.last_dump_time > dump_period):
            self.last_dump_time = ts_float
            run = archive_run(self.routine, self.data, self.states)
            try:
                path = run['path']
                filename = run['filename'][:-4] + 'pickle'
                self.env.interface.stop_recording(os.path.join(path, filename))
            except:
                pass

        # Take a break to let the outside signal to change the status
        time.sleep(0.1)

        # Check if termination condition has been satisfied
        if self.termination_condition is None:
            return

        tc_config = self.termination_condition
        idx = tc_config['tc_idx']
        if idx == 0:
            max_eval = tc_config['max_eval']
            if self.data.shape[0] >= max_eval:
                raise BadgerRunTerminatedError

        elif idx == 1:
            max_time = tc_config['max_time']
            dt = time.time() - self.start_time
            if dt >= max_time:
                raise BadgerRunTerminatedError
        # elif idx == 2:
        #     ftol = tc_config['ftol']
        #     # Do something

    def run_status(self):
        if self.is_killed:
            return 2
        elif self.is_paused:
            return 1
        else:
            return 0  # running

    def before_evaluate_xopt(self, candidates: DataFrame):
        pass

    def after_evaluate_xopt(self, data: DataFrame):
        vars = data[self.var_names].to_numpy()[0]
        obses = data[self.obj_names].to_numpy()[0]
        cons = data[self.con_names].to_numpy()
        try:
            cons = cons[0]
        except IndexError:
            pass
        stas = data[self.sta_names].to_numpy()
        try:
            stas = stas[0]
        except IndexError:
            pass
        self.after_evaluate(vars, obses, cons, stas)

    def env_ready(self, env):
        self.env = env
        var_dict = env._get_variables(self.var_names)
        init_vars = [var_dict[v] for v in self.var_names]
        self.signals.env_ready.emit(init_vars)

    def pf_ready(self, pf):
        self.pf = pf

    def states_ready(self, states):
        self.states = states

    def ctrl_routine(self, pause):
        self.is_paused = pause

    def stop_routine(self):
        self.is_killed = True
