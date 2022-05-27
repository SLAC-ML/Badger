import numpy as np
from multiprocessing.managers import BaseManager
import logging
logger = logging.getLogger(__name__)
from .utils import range_to_str, yprint, merge_params, ParetoFront, norm, denorm


class BadgerManager(BaseManager):
    pass


def normalize_routine(routine):
    # Sanity check and config normalization
    #
    # routine
    #  name
    #  algo
    #  env
    #  algo_params
    #  env_params
    #  env_vranges: use for vars normalization in config
    #  config: change the var ranges, the obj rules, and the constraints
    env_vranges = routine['env_vranges']
    config = routine['config']

    # Normalize the variables
    for i, var in enumerate(config['variables']):
        if type(var) is str:
            config['variables'][i] = _dict = {}
            _dict[var] = env_vranges[var]
        else:
            var_name = next(iter(var))  # get the only (first) key in the dict
            vrange_vocs = var[var_name]
            vrange_default = env_vranges[var_name]

            if vrange_vocs is None:
                var[var_name] = vrange_default
                continue

            if vrange_vocs[0] < vrange_default[0]:
                logger.warning(
                    f'variable {var_name}: lower limit {vrange_vocs[0]} exceeds the bound, set to the lower bound {vrange_default[0]}')
                lb = vrange_default[0]
            else:
                lb = vrange_vocs[0]
            if vrange_vocs[1] > vrange_default[1]:
                logger.warning(
                    f'variable {var_name}: upper limit {vrange_vocs[1]} exceeds the bound, set to the upper bound {vrange_default[1]}')
                ub = vrange_default[1]
            else:
                ub = vrange_vocs[1]

            if lb >= ub:  # TODO: add logic to deal with the == condition
                raise Exception(
                    f'variable {var_name}: lower limit {lb} must be lower than the upper limit {ub}!')
            var[var_name] = [lb, ub]

    # Normalize the objectives
    for i, obj in enumerate(config['objectives']):
        if type(obj) is str:
            config['objectives'][i] = _dict = {}
            _dict[obj] = 'MINIMIZE'
        else:
            obj_name = next(iter(obj))
            if obj[obj_name] is None:
                obj[obj_name] = 'MINIMIZE'

    # Normalize the constraints
    try:
        _ = config['constraints']
        if not _:  # empty list
            config['constraints'] = None
    except KeyError:
        config['constraints'] = None

    # Remove the additional info
    del routine['env_vranges']

    return routine


def run_routine(routine, skip_review=False, save=None, verbose=2,
                before_evaluate=None, after_evaluate=None,
                env_ready=None, pf_ready=None):
    # Review the routine
    if not skip_review:
        print('Please review the routine to be run:\n')

        routine_configs_var = routine['config']['variables']
        routine['config']['variables'] = range_to_str(routine_configs_var)
        print('=== Optimization Routine ===')
        yprint(routine)
        print('')

        while True:
            res = input('Proceed ([y]/n)? ')
            if res == 'n':
                return
            elif (not res) or (res == 'y'):
                break
            else:
                print(f'Invalid choice: {res}')

        routine['config']['variables'] = routine_configs_var

    # Save routine if specified
    if save:
        import sqlite3
        from .db import save_routine

        try:
            save_routine(routine)
        except sqlite3.IntegrityError:
            raise Exception(
                f'Routine {routine["name"]} already existed in the database! Please choose another name.')

    # Set up and run the optimization
    from .factory import get_algo, get_env

    # Instantiate the environment
    Environment, configs_env = get_env(routine['env'])
    _configs_env = merge_params(
        configs_env, {'params': routine['env_params']})
    parallel = not is_sync_mode(_configs_env)  # if run in sync mode

    if parallel:  # register the interface for multiprocessing
        register_intf(_configs_env)

    with BadgerManager() as manager:
        # if not parallel:
        manager = None

        env = instantiate_env(Environment, _configs_env, manager)
        if env_ready:
            env_ready(env)

        optimize, configs_algo = get_algo(routine['algo'])

        from .logger import _get_default_logger
        from .logger.event import Events

        # log the optimization progress
        opt_logger = _get_default_logger(verbose)
        var_names = [next(iter(d)) for d in routine['config']['variables']]
        vranges = np.array([d[next(iter(d))]
                            for d in routine['config']['variables']])
        obj_names = [next(iter(d)) for d in routine['config']['objectives']]
        rules = [d[next(iter(d))] for d in routine['config']['objectives']]
        pf = ParetoFront(rules)
        if pf_ready:
            pf_ready(pf)
        if routine['config']['constraints']:
            con_names = [next(iter(d))
                         for d in routine['config']['constraints']]
            thresholds = [d[next(iter(d))]
                          for d in routine['config']['constraints']]
        else:
            con_names = []
            thresholds = []

        info = {'count': -1}
        # Make a normalized evaluate function

        def evaluate(X):
            Y = []  # objectives
            I = []  # inequality constraints
            E = []  # equality constraints
            Xo = []  # normalized readback of variables

            # Return current state if X is None
            # Do not do the evaluation due to possible high cost
            if X is None:
                _x = np.array(env._get_vars(var_names))
                x = norm(_x, vranges[:, 0], vranges[:, 1])
                X = x.reshape(1, -1)
                return None, None, None, X

            # Check if bounds are violated
            if np.max(X) > 1 or np.min(X) < 0:
                logger.warning('proposed trial solution exceeds the bounds, solution has been clipped at bounds!')
                X = np.clip(X, 0, 1)

            for x in X:
                _x = denorm(x, vranges[:, 0], vranges[:, 1])

                # Use unsafe version to support temp vars
                # We have to trust the users...
                env._set_vars(var_names, _x)
                env.vars_changed(var_names, _x)

                _xo = np.array(env._get_vars(var_names), dtype=np.float64)
                xo = norm(_xo, vranges[:, 0], vranges[:, 1])
                Xo.append(xo)

                # Return the readback rather than the values to be set
                if before_evaluate:
                    before_evaluate(_xo)

                # Deal with objectives
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
                obses_raw = np.array(obses_raw, dtype=np.float64)

                # Deal with constraints
                # TODO: Check overlapping between objs and cons
                cons_i = []
                cons_e = []
                cons_raw = []
                for i, con_name in enumerate(con_names):
                    relation, thres = thresholds[i][:2]
                    con = float(env.get_obs(con_name))
                    if relation == 'GREATER_THAN':
                        cons_i.append(con - thres)
                    elif relation == 'LESS_THAN':
                        cons_i.append(thres - con)
                    else:
                        cons_e.append(con - thres)
                    cons_raw.append(con)
                if cons_i:
                    I.append(cons_i)
                if cons_e:
                    E.append(cons_e)
                cons_raw = np.array(cons_raw, dtype=np.float64)

                info['count'] += 1
                _idx_x = np.insert(_xo, 0, info['count'])  # keep the idx info

                is_optimal = not pf.is_dominated((_idx_x, obses_raw))
                solution = (_xo, obses_raw, cons_raw, is_optimal,
                            var_names, obj_names, con_names)
                opt_logger.update(Events.OPTIMIZATION_STEP, solution)

                if after_evaluate:
                    after_evaluate(_xo, obses_raw, cons_raw)

            Y = np.array(Y)
            if I:
                I = np.array(I)
            else:
                I = None
            if E:
                E = np.array(E)
            else:
                E = None
            Xo = np.array(Xo)

            return Y, I, E, Xo

        # Start the optimization
        print('')
        solution = (None, None, None, None, var_names, obj_names, con_names)
        opt_logger.update(Events.OPTIMIZATION_START, solution)
        try:
            if not callable(optimize):  # doing optimization through extensions
                configs = {
                    'routine_configs': routine['config'],
                    'algo_configs': merge_params(configs_algo, {'params': routine['algo_params']}),
                    'env_configs': _configs_env,
                }
                optimize = optimize.optimize
            else:
                configs = routine['algo_params']

            optimize(evaluate, configs)
        except Exception as e:
            opt_logger.update(Events.OPTIMIZATION_END, solution)
            raise e
        opt_logger.update(Events.OPTIMIZATION_END, solution)


def is_sync_mode(configs):
    try:
        is_sync = configs['params']['sync']
    except KeyError:
        is_sync = False
    except TypeError:
        is_sync = False
    except Exception as e:
        logger.warning(e)
        is_sync = False

    return is_sync


def register_intf(configs):
    from .factory import get_intf  # have to put here to avoid circular dependencies

    try:
        intf_name = configs['interface'][0]
    except KeyError:
        intf_name = None
    except Exception as e:
        logger.warning(e)
        intf_name = None

    if intf_name is not None:
        Interface, _ = get_intf(intf_name)
        BadgerManager.register('Interface', Interface)


def instantiate_env(env_class, configs, manager=None):
    from .factory import get_intf  # have to put here to avoid circular dependencies

    # Configure interface
    # TODO: figure out the correct logic
    # It seems that the interface should be given rather than
    # initialized here
    try:
        intf_name = configs['interface'][0]
    except KeyError:
        intf_name = None
    except Exception as e:
        logger.warning(e)
        intf_name = None

    if intf_name is not None:
        if manager is None:
            Interface, _ = get_intf(intf_name)
            intf = Interface()
        else:
            intf = manager.Interface()
    else:
        intf = None

    env = env_class(intf, configs['params'])

    return env
