import os
import sys
import logging
from .utils import curr_ts_to_str, ystring


# Check badger optimization run archive root
BADGER_RUN_ROOT = os.getenv('BADGER_RUN_ROOT')
if BADGER_RUN_ROOT is None:
    logging.error('Please set the BADGER_RUN_ROOT env var!')
    sys.exit()
elif not os.path.exists(BADGER_RUN_ROOT):
    os.makedirs(BADGER_RUN_ROOT)
    logging.info(
        f'Badger run root {BADGER_RUN_ROOT} created')


def archive_run(routine, data):
    # routine: dict
    # data: pandas dataframe
    run = {
        'routine': routine,
        'data': data.to_dict('list'),
    }

    fname = f'BadgerOpt-{curr_ts_to_str("lcls-fname")}.yaml'
    with open(os.path.join(BADGER_RUN_ROOT, fname), 'w') as f:
        f.write(ystring(run))


def list_run():
    return [p for p in os.listdir(BADGER_RUN_ROOT) if os.path.splitext(p)[1] == '.yaml']
