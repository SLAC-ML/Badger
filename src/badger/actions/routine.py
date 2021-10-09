from ..db import load_routine, list_routines
from ..utils import range_to_str, yprint


def show_routine(args):
    if args.routine_name is None:
        yprint(list_routines())
    else:
        routine = load_routine(args.routine_name)
        if routine is not None:
            routine['config']['variables'] = range_to_str(routine['config']['variables'])
            yprint(routine)
