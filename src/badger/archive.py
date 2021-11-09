import os
import logging
logger = logging.getLogger(__name__)
from .utils import curr_ts_to_str, ystring, load_config
from .settings import read_value


# Check badger optimization run archive root
BADGER_ARCHIVE_ROOT = read_value('BADGER_ARCHIVE_ROOT')
if BADGER_ARCHIVE_ROOT is None:
    raise Exception('Please set the BADGER_ARCHIVE_ROOT env var!')
elif not os.path.exists(BADGER_ARCHIVE_ROOT):
    os.makedirs(BADGER_ARCHIVE_ROOT)
    logger.info(
        f'Badger run root {BADGER_ARCHIVE_ROOT} created')


def archive_run(routine, data):
    # routine: dict
    # data: pandas dataframe
    run = {
        'routine': routine,
        'data': data.to_dict('list'),
    }

    suffix = curr_ts_to_str("lcls-fname")
    tokens = suffix.split('-')
    first_level = tokens[0]
    second_level = f'{tokens[0]}-{tokens[1]}'
    third_level = f'{tokens[0]}-{tokens[1]}-{tokens[2]}'
    path = os.path.join(BADGER_ARCHIVE_ROOT, first_level, second_level, third_level)
    os.makedirs(path, exist_ok=True)
    fname = f'BadgerOpt-{suffix}.yaml'
    with open(os.path.join(path, fname), 'w') as f:
        f.write(ystring(run))


def list_run():
    runs = {}
    # Get years, latest first
    years = sorted([p for p in os.listdir(BADGER_ARCHIVE_ROOT)
                   if os.path.isdir(os.path.join(BADGER_ARCHIVE_ROOT, p))], reverse=True)
    for year in years:
        path_year = os.path.join(BADGER_ARCHIVE_ROOT, year)
        months = sorted([p for p in os.listdir(path_year) if os.path.isdir(
            os.path.join(path_year, p))], reverse=True)
        runs[year] = {}
        for month in months:
            path_month = os.path.join(path_year, month)
            days = sorted([p for p in os.listdir(path_month) if os.path.isdir(
                os.path.join(path_month, p))], reverse=True)
            runs[year][month] = {}
            for day in days:
                path_day = os.path.join(path_month, day)
                files = [p for p in os.listdir(path_day) if os.path.splitext(p)[
                    1] == '.yaml']
                files = sorted(files, key=lambda f: os.path.getmtime(
                    os.path.join(path_day, f)), reverse=True)
                runs[year][month][day] = files

    return runs


def load_run(run_fname):
    tokens = run_fname.split('-')
    first_level = tokens[1]
    second_level = f'{tokens[1]}-{tokens[2]}'
    third_level = f'{tokens[1]}-{tokens[2]}-{tokens[3]}'

    return load_config(os.path.join(BADGER_ARCHIVE_ROOT, first_level, second_level, third_level, run_fname))
