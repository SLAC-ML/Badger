import logging
import time
from typing import Callable

import numpy as np
from pandas import concat, DataFrame

from badger.errors import (
    BadgerRunTerminatedError,
)
from badger.routine import Routine
from badger.utils import (
    curr_ts_to_str,
    dump_state,
    ParetoFront,
)


def evaluate_points(
        points: DataFrame, routine: Routine, callback: Callable
) -> DataFrame:
    """
    Evaluates points using the environment

    Parameters
    ----------
    points : DataFrame
    routine : Routine
    callback : Callable

    Returns
    -------
    evaluated_points : DataFrame
    """

    env = routine.environment
    vocs = routine.vocs

    obj_list = []
    for i in range(points.shape[0]):
        env._set_variables(points.iloc[i].to_dict())  # point is a series!
        obj = env._get_observables(vocs.objective_names)
        obj_df = DataFrame(obj, index=[0])
        obj_list.append(obj_df)

        # Have to call the callback after each evaluation
        # since we need the time information
        # Note: point here is a dataframe!
        point_eval = concat([points.iloc[i:i + 1].reset_index(drop=True),
                             obj_df], axis=1)
        if callback:
            callback(point_eval)

    points_obj = concat(obj_list, axis=0).reset_index(drop=True)
    points_eval = concat([points, points_obj], axis=1)

    return points_eval


def add_to_pf(idx: int, candidate: DataFrame, result: DataFrame,
              pf: ParetoFront) -> None:
    n_sol, n_var = candidate.shape
    for i in range(n_sol):  # loop through each solution
        inputs = candidate.iloc[i].values
        inputs = np.insert(inputs, 0, idx + i)
        outputs = result.iloc[i][n_var:].values[:]  # copy to avoid troubles
        pf.is_dominated((inputs, outputs))

    return n_sol  # number of points inserted


def check_run_status(active_callback):
    while True:
        status = active_callback()
        if status == 2:
            raise BadgerRunTerminatedError
        elif status == 1:
            time.sleep(0)
            continue
        else:
            break


def run_routine(
        routine: Routine,
        active_callback: Callable,
        generate_callback: Callable,
        evaluate_callback: Callable,
        states_callback: Callable,
        dump_file_callback: Callable = None,
) -> None:
    """
    Run the provided routine object using Xopt.

    Parameters
    ----------
    routine : Routine
        Routine object created by Badger GUI to run optimization.

    active_callback : Callable
        Callback function that returns an int denoting if
        optimization/evaluation should proceed.
        0: proceed
        1: paused
        2: killed

    generate_callback : Callable
        Callback function called after generating candidate points that takes
        the form `f(generator: Generator, candidates: DataFrame)`.

    evaluate_callback : Callable
        Callback function called after evaluating points that takes the form
        `f(data: DataFrame)`.

    pf_callback : Callable
        Callback function called after Pareto Front object is instantiated

    states_callback : Callable
        Callback function called after system states is fetched
    """

    environment = routine.environment
    initial_points = routine.initial_points

    # Save system states if applicable
    states = environment.get_system_states()
    if states_callback and (states is not None):
        states_callback(states)

    # evaluate initial points:
    # Nikita: more care about the setting var logic,
    # wait or consider timeout/retry
    result = evaluate_points(initial_points, routine, evaluate_callback)

    # add measurements to generator
    routine.generator.add_data(result)

    # Prepare for dumping file
    if dump_file_callback:
        combined_results = None
        ts_start = curr_ts_to_str()
        dump_file = dump_file_callback()
        if not dump_file:
            dump_file = f"xopt_states_{ts_start}.yaml"

    # perform optimization
    while True:
        status = active_callback()
        if status == 2:
            raise BadgerRunTerminatedError
        elif status == 1:
            time.sleep(0)
            continue

        # generate points to observe
        candidates = routine.generate(1)[0]
        candidates = DataFrame(candidates, index=[0])
        # generate_callback(generator, candidates)
        generate_callback(candidates)

        check_run_status(active_callback)
        # if still active evaluate the points and add to generator
        # check active_callback evaluate point
        result = evaluate_points(candidates, routine, evaluate_callback)

        # Dump Xopt state after each step
        if dump_file_callback:
            if combined_results is not None:
                combined_results = concat(
                    [combined_results, result], axis=0).reset_index(drop=True)
            else:
                combined_results = result

            dump_state(dump_file, routine.generator, combined_results)

        # Add data to generator
        routine.add_data(result)
