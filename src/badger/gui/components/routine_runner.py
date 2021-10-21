import time
import numpy as np
# from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtCore import pyqtSignal, QObject, QRunnable


class BadgerRoutineSignals(QObject):
    finished = pyqtSignal()
    progress = pyqtSignal(list, list)


class BadgerRoutineRunner(QRunnable):

    signals = BadgerRoutineSignals()

    def __init__(self, routine, save, verbose=2):
        super().__init__()

        self.routine = routine
        self.save = save
        self.verbose = verbose

        self.is_paused = False
        self.is_killed = False

    def run(self):
        try:
            self._run()
        except Exception as e:
            print(e)
            # QMessageBox.critical(None, 'Error!', str(e))

        self.signals.finished.emit()

    def _run(self):
        save = self.save
        routine = self.routine
        verbose = self.verbose

        # Save routine if specified
        if save:
            import sqlite3
            from ...db import save_routine

            try:
                save_routine(routine)
            except sqlite3.IntegrityError:
                raise Exception(
                    f'Routine {routine["name"]} already existed in the database! Please choose another name.')

        # Set up and run the optimization
        from ...factory import get_algo, get_intf, get_env
        from ...utils import merge_params, ParetoFront, denorm

        Environment, configs_env = get_env(routine['env'])
        try:
            intf_name = configs_env['interface'][0]
            Interface, _ = get_intf(intf_name)
            intf = Interface()
        except Exception:
            intf = None
        env = Environment(intf, routine['env_params'])

        optimize, configs_algo = get_algo(routine['algo'])
        if not callable(optimize):  # Doing optimization through extensions
            configs = {
                'routine_configs': routine['config'],
                'algo_configs': merge_params(configs_algo, {'params': routine['algo_params']})
            }
            optimize.run(env, configs)
            print('done!')
        else:
            from ...logger import _get_default_logger
            from ...logger.event import Events

            # log the optimization progress
            logger = _get_default_logger(verbose)
            var_names = [next(iter(d)) for d in routine['config']['variables']]
            vranges = np.array([d[next(iter(d))]
                                for d in routine['config']['variables']])
            obj_names = [next(iter(d))
                         for d in routine['config']['objectives']]
            rules = [d[next(iter(d))] for d in routine['config']['objectives']]
            pf = ParetoFront(rules)

            # Make a normalized evaluate function
            def evaluate(X):
                Y = []
                for x in X:
                    while self.is_paused:
                        time.sleep(0)
                        if self.is_killed:
                            raise Exception('Optimization run has been terminated!')

                    if self.is_killed:
                        raise Exception('Optimization run has been terminated!')

                    _x = denorm(x, vranges[:, 0], vranges[:, 1])
                    env.set_vars(var_names, _x)
                    obses = []
                    obses_raw = []
                    for i, obj_name in enumerate(obj_names):
                        rule = rules[i]
                        obs = float(env.get_obs(obj_name))
                        if rule == 'MAXIMIZE':
                            obses.append(-obs)
                        else:
                            obses.append(obs)
                        obses_raw.append(obs)
                    Y.append(obses)
                    obses_raw = np.array(obses_raw)
                    is_optimal = not pf.is_dominated((_x, obses_raw))
                    solution = (_x, obses_raw, is_optimal,
                                var_names, obj_names)
                    logger.update(Events.OPTIMIZATION_STEP, solution)
                    self.signals.progress.emit(list(_x), list(obses_raw))

                    # take a break to let the outside signal to change the status
                    time.sleep(0.1)

                Y = np.array(Y)

                return Y, None, None

            solution = (None, None, None, var_names, obj_names)
            print('')

            logger.update(Events.OPTIMIZATION_START, solution)
            try:
                optimize(evaluate, routine['algo_params'])
            except Exception as e:
                logger.update(Events.OPTIMIZATION_END, solution)
                raise e
            logger.update(Events.OPTIMIZATION_END, solution)

    def ctrl_routine(self, pause):
        self.is_paused = pause

    def stop_routine(self):
        self.is_killed = True
