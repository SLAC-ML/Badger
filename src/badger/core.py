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
    # TODO: need to evaluate a single point at the time
    for index, ele in initial_points.iterrows():
        routine.evaluate_data(ele.to_dict())

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
        candidates = routine.generator.generate(1)[0]
        candidates = DataFrame(candidates, index=[0])
        # generate_callback(generator, candidates)
        generate_callback(candidates)

        check_run_status(active_callback)
        # if still active evaluate the points and add to generator
        # check active_callback evaluate point
        result = routine.evaluate_data(candidates)

        # Dump Xopt state after each step
        if dump_file_callback:
            if combined_results is not None:
                combined_results = concat(
                    [combined_results, result], axis=0).reset_index(drop=True)
            else:
                combined_results = result

            dump_state(dump_file, routine.generator, combined_results)
