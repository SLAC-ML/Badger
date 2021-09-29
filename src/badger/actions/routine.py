from ..db import load_routine, list_routines
from ..utils import yprint


def show_routine(args):
    if args.routine_name is None:
        yprint(list_routines())
    else:
        routine = load_routine(args.routine_name)
        if routine is not None:
            yprint(routine)
