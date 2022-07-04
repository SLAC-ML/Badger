import logging
logger = logging.getLogger(__name__)
import time
import pandas as pd
from PyQt5.QtCore import pyqtSignal, QObject, QRunnable
from ...utils import curr_ts, ts_to_str
from ...core import run_routine


class BadgerRoutineSignals(QObject):
    env_ready = pyqtSignal(list)
    finished = pyqtSignal()
    progress = pyqtSignal(list, list, list, list, float)
    error = pyqtSignal(Exception)
    info = pyqtSignal(str)


class BadgerRoutineRunner(QRunnable):

    def __init__(self, routine, save, verbose=2, use_full_ts=False):
        super().__init__()

        # Signals should belong to instance rather than class
        # Since there could be multiple runners runing in parallel
        self.signals = BadgerRoutineSignals()

        self.routine = routine
        self.run_filename = None
        self.var_names = var_names = [next(iter(d)) for d in routine['config']['variables']]
        self.obj_names = obj_names = [next(iter(d)) for d in routine['config']['objectives']]
        if routine['config']['constraints']:
            self.con_names = con_names = [next(iter(d)) for d in routine['config']['constraints']]
        else:
            self.con_names = con_names = []
        try:
            self.sta_names = sta_names = routine['config']['states'] or []
        except KeyError:  # this would happen when rerun an old version routine
            self.sta_names = sta_names = []
        self.data = pd.DataFrame(None, columns=['timestamp_raw', 'timestamp'] + obj_names + con_names + var_names + sta_names)
        self.states = None  # system states to be saved at start of a run
        self.save = save
        self.verbose = verbose
        self.use_full_ts = use_full_ts

        self.is_paused = False
        self.is_killed = False

    def run(self):
        error = None
        try:
            run_routine(self.routine, True, self.save, self.verbose,
                        self.before_evaluate, self.after_evaluate,
                        self.env_ready, self.pf_ready, self.states_ready)
        except Exception as e:
            if str(e) != 'Optimization run has been terminated!':
                logger.exception(e)
            error = e

        self.signals.finished.emit()
        if error:
            if str(error) == 'Optimization run has been terminated!':
                self.signals.info.emit(str(error))
                return

            self.signals.error.emit(error)

    def before_evaluate(self, vars):
        # vars: ndarray
        while self.is_paused:
            time.sleep(0)
            if self.is_killed:
                raise Exception('Optimization run has been terminated!')

        if self.is_killed:
            raise Exception('Optimization run has been terminated!')

    def after_evaluate(self, vars, obses, cons, stas):
        # vars: ndarray
        # obses: ndarray
        # cons: ndarray
        # stas: list
        ts = curr_ts()
        self.signals.progress.emit(list(vars), list(obses), list(cons), list(stas), ts.timestamp())

        # Append solution to data
        fmt = 'lcls-log-full' if self.use_full_ts else 'lcls-log'
        solution = [ts.timestamp(), ts_to_str(ts, fmt)] + list(obses) + list(cons) + list(vars) + list(stas)
        self.data = self.data.append(pd.Series(solution, index=self.data.columns), ignore_index=True)

        # take a break to let the outside signal to change the status
        time.sleep(0.1)

    def env_ready(self, env):
        self.env = env
        init_vars = env._get_vars(self.var_names)
        self.signals.env_ready.emit(init_vars)

    def pf_ready(self, pf):
        self.pf = pf

    def states_ready(self, states):
        self.states = states

    def ctrl_routine(self, pause):
        self.is_paused = pause

    def stop_routine(self):
        self.is_killed = True
