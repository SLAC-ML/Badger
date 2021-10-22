import time
from PyQt5.QtCore import pyqtSignal, QObject, QRunnable
from ...utils import run_routine


class BadgerRoutineSignals(QObject):
    finished = pyqtSignal()
    progress = pyqtSignal(list, list)
    error = pyqtSignal(AssertionError)


class BadgerRoutineRunner(QRunnable):

    def __init__(self, routine, save, verbose=2):
        super().__init__()

        # Signals should belong to instance rather than class
        # Since there could be multiple runners runing in parallel
        self.signals = BadgerRoutineSignals()

        self.routine = routine
        self.save = save
        self.verbose = verbose

        self.is_paused = False
        self.is_killed = False

    def run(self):
        error = None
        try:
            run_routine(self.routine, True, self.save, self.verbose,
                        self.before_evaluate, self.after_evaluate)
        except Exception as e:
            error = e

        self.signals.finished.emit()
        if error:
            self.signals.error.emit(error)

    def before_evaluate(self, vars):
        # vars: ndarray
        while self.is_paused:
            time.sleep(0)
            if self.is_killed:
                raise Exception('Optimization run has been terminated!')

        if self.is_killed:
            raise Exception('Optimization run has been terminated!')

    def after_evaluate(self, vars, obses):
        # vars: ndarray
        # obses: ndarray
        self.signals.progress.emit(list(vars), list(obses))

        # take a break to let the outside signal to change the status
        time.sleep(0.1)

    def ctrl_routine(self, pause):
        self.is_paused = pause

    def stop_routine(self):
        self.is_killed = True
