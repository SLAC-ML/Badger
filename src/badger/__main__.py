import argparse

from .actions.doctor import self_check
from .actions.routine import show_routine
from .actions.algo import show_algo
from .actions.env import show_env
from .actions.intf import show_intf
from .actions.run import run_routine


def main():
    # Create the top-level parser
    parser = argparse.ArgumentParser(description='Badger the optimizer')
    subparsers = parser.add_subparsers(help='Badger commands help')

    # Parser for the 'doctor' command
    parser_doctor = subparsers.add_parser(
        'doctor', help='Badger status self-check')
    parser_doctor.set_defaults(func=self_check)

    # Parser for the 'routine' command
    parser_routine = subparsers.add_parser('routine', help='Badger routines')
    parser_routine.set_defaults(func=show_routine)

    # Parser for the 'algo' command
    parser_algo = subparsers.add_parser('algo', help='Badger algorithms')
    parser_algo.set_defaults(func=show_algo)

    # Parser for the 'intf' command
    parser_intf = subparsers.add_parser('intf', help='Badger interfaces')
    parser_intf.set_defaults(func=show_intf)

    # Parser for the 'env' command
    parser_env = subparsers.add_parser('env', help='Badger environments')
    parser_env.set_defaults(func=show_env)

    # Parser for the 'run' command
    parser_run = subparsers.add_parser('run', help='Run routines')
    parser_run.set_defaults(func=run_routine)

    args = parser.parse_args()
    args.func(args)


if __name__ == '__main__':
    main()
