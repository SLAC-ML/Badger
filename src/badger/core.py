import time
import logging
from typing import Callable
from pandas import DataFrame, concat
from pydantic import BaseModel
from xopt import Generator
from badger.environment import Environment
from badger.utils import ParetoFront, parse_rule, curr_ts_to_str, dump_state
logger = logging.getLogger(__name__)


class Routine(BaseModel):
    environment: Environment
    generator: Generator
    initial_points: DataFrame

    class Config:
        arbitrary_types_allowed = True

    # convenience properties
    @property
    def vocs(self):
        """
        A property that returns the vocs of the generator attribute.

        Returns:
            self.generator.vocs : VOCS
        """
        return self.generator.vocs


def evaluate_points(points: DataFrame, routine: Routine, callback: Callable) \
        -> DataFrame:
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
    for _, point in points.iterrows():
        env.set_variables(point.to_dict())
        obj = env.get_observables(vocs.objective_names)
        obj_df = DataFrame(obj, index=[0])
        obj_list.append(obj_df)
    points_obj = concat(obj_list, axis=0).reset_index(drop=True)
    points_eval = concat([points, points_obj], axis=1)

    if callback:
        callback(points_eval)

    return points_eval


def run_routine_xopt(
        routine: Routine,
        active_callback: Callable,
        generate_callback: Callable,
        evaluate_callback: Callable,
        pf_callback: Callable,
        states_callback: Callable,
        dump_file_callback: Callable,
        ) -> None:
    """
    Run the provided routine object using Xopt.

    Parameters
    ----------
    routine : Routine
        Routine object created by Badger GUI to run optimization.

    active_callback : Callable
        Callback function that returns an int denoting if optimization/evaluation
        should proceed.
        0: proceed
        1: paused
        2: killed

    generate_callback : Callable
        Callback function called after generating candidate points that takes the form
        `f(generator: Generator, candidates: DataFrame)`.

    evaluate_callback : Callable
        Callback function called after evaluating points that takes the form `f(data:
        DataFrame)`.

    pf_callback : Callable
        Callback function called after Pareto Front object is instantiated

    states_callback : Callable
        Callback function called after system states is fetched
    """

    environment = routine.environment
    generator = routine.generator
    initial_points = routine.initial_points

    # Setup Pareto front: soon to die
    directions = [parse_rule(rule)['direction'] for rule in routine.vocs.objectives.values()]
    pf = ParetoFront(directions)
    if pf_callback:
        pf_callback(pf)

    # Save system states if applicable
    states = environment.get_system_states()
    if states_callback and (states is not None):
        states_callback(states)

    # evaluate initial points:
    # Nikita: more care about the setting var logic, wait or consider timeout/retry
    result = evaluate_points(initial_points, routine, evaluate_callback)

    # add measurements to generator
    generator.add_data(result)
    
    combined_results = None 
    # perform optimization
    while True:
        status = active_callback()
        if status == 2:
            raise Exception('Optimization run has been terminated!')
        elif status == 1:
            time.sleep(0)
            continue

        # generate points to observe
        candidates = generator.generate(1)
        # generate_callback(generator, candidates)
        generate_callback(candidates)

        # if still active evaluate the points and add to generator
        # check active_callback evaluate point
        result = evaluate_points(candidates, routine, evaluate_callback)

        if combined_results:
            combined_results = combined_results.concat(result)
        else:
            combined_results = result

        if dump_file_callback:
            file_name = dump_file_callback()
        else:
            file_name = "routine_results" + curr_ts_to_str() + ".yaml"
        
        dump_state(file_name, generator, combined_results)
        

        # Add data to generator
        generator.add_data(result)


def gui_to_routine(routine: dict) -> Routine:
    pass
