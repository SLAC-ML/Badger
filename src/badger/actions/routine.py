from ..db import load_routine, list_routines
from ..utils import range_to_str, yprint, run_routine


def show_routine(args):
    # List routines
    if args.routine_name is None:
        yprint(list_routines())
        return

    routine = load_routine(args.routine_name)
    if routine is None:
        return

    # Print the routine
    if not args.run:
        routine['config']['variables'] = range_to_str(routine['config']['variables'])
        yprint(routine)
        return

    # Run the routine
    run_routine(routine, args.yes, None, args.verbose)
