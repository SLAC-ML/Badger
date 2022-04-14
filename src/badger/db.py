import os
from datetime import datetime
import logging
logger = logging.getLogger(__name__)
import yaml
import sqlite3
from .settings import read_value


# Check badger database root
BADGER_DB_ROOT = read_value('BADGER_DB_ROOT')
if BADGER_DB_ROOT is None:
    raise Exception('Please set the BADGER_DB_ROOT env var!')
elif not os.path.exists(BADGER_DB_ROOT):
    os.makedirs(BADGER_DB_ROOT)
    logger.info(
        f'Badger database root {BADGER_DB_ROOT} created')


def save_routine(routine):
    db_routine = os.path.join(BADGER_DB_ROOT, 'routines.db')

    # Initialize
    if not os.path.exists(db_routine):
        con = sqlite3.connect(db_routine)
        cur = con.cursor()
        cur.execute('create table routine (name not null primary key, config, savedAt timestamp)')
    else:
        con = sqlite3.connect(db_routine)
        cur = con.cursor()

    # Insert a record
    try:
        cur.execute('insert into routine values (?, ?, ?)',
                    (routine['name'], yaml.dump(routine, sort_keys=False), datetime.now()))
    except sqlite3.OperationalError:
        cur.execute('create table routine (name not null primary key, config, savedAt timestamp)')
        cur.execute('insert into routine values (?, ?, ?)',
                    (routine['name'], yaml.dump(routine, sort_keys=False), datetime.now()))
    con.commit()
    con.close()


def remove_routine(name, remove_runs=False):
    db_routine = os.path.join(BADGER_DB_ROOT, 'routines.db')

    con = sqlite3.connect(db_routine)
    cur = con.cursor()

    cur.execute(f'delete from routine where name = "{name}"')

    con.commit()
    con.close()

    if remove_runs:
        # Remove all related run records
        db_run = os.path.join(BADGER_DB_ROOT, 'runs.db')

        con = sqlite3.connect(db_run)
        cur = con.cursor()

        cur.execute(f'delete from run where routine = "{name}"')

        con.commit()
        con.close()


def load_routine(name):
    db_routine = os.path.join(BADGER_DB_ROOT, 'routines.db')
    con = sqlite3.connect(db_routine)
    cur = con.cursor()

    try:
        cur.execute('select * from routine where name=:name', {'name': name})
    except sqlite3.OperationalError:
        cur.execute('create table routine (name not null primary key, config, savedAt timestamp)')
        cur.execute('select * from routine where name=:name', {'name': name})
    records = cur.fetchall()
    con.close()

    if len(records) == 1:
        return yaml.safe_load(records[0][1]), records[0][2]
    elif len(records) == 0:
        # logger.warning(f'Routine {name} not found in the database!')
        return None, None
    else:
        raise Exception(
            f'Multiple routines with name {name} found in the database!')


def list_routine(keyword=''):
    db_routine = os.path.join(BADGER_DB_ROOT, 'routines.db')
    con = sqlite3.connect(db_routine)
    cur = con.cursor()

    try:
        cur.execute(f'select name, savedAt from routine where name like "%{keyword}%" order by savedAt desc')
    except sqlite3.OperationalError:
        cur.execute('create table routine (name not null primary key, config, savedAt timestamp)')
        cur.execute(f'select name, savedAt from routine where name like "%{keyword}%" order by savedAt desc')
    records = cur.fetchall()
    names = [record[0] for record in records]
    timestamps = [record[1] for record in records]
    con.close()

    return names, timestamps


def save_run(run):
    db_run = os.path.join(BADGER_DB_ROOT, 'runs.db')

    # Initialize
    if not os.path.exists(db_run):
        con = sqlite3.connect(db_run)
        cur = con.cursor()
        cur.execute('create table run (id integer primary key, savedAt timestamp, finishedAt timestamp, routine, filename)')
    else:
        con = sqlite3.connect(db_run)
        cur = con.cursor()

    # Insert a record
    routine_name = run['routine']['name']
    run_filename = run['filename']
    timestamps = run['data']['timestamp_raw']
    time_start = datetime.fromtimestamp(timestamps[0])
    time_finish = datetime.fromtimestamp(timestamps[-1])
    try:
        cur.execute('insert into run values (?, ?, ?, ?, ?)',
                    (None, time_start, time_finish, routine_name, run_filename))
    except sqlite3.OperationalError:
        cur.execute('create table run (id integer primary key, savedAt timestamp, finishedAt timestamp, routine, filename)')
        cur.execute('insert into run values (?, ?, ?, ?, ?)',
                    (None, time_start, time_finish, routine_name, run_filename))
    rid = cur.lastrowid

    con.commit()
    con.close()

    return rid


def get_runs_by_routine(routine: str):
    db_run = os.path.join(BADGER_DB_ROOT, 'runs.db')

    con = sqlite3.connect(db_run)
    cur = con.cursor()

    cur.execute(f'select filename from run where routine = "{routine}" order by savedAt desc')
    records = cur.fetchall()
    con.close()

    filenames = [record[0] for record in records]

    return filenames


def get_runs():
    db_run = os.path.join(BADGER_DB_ROOT, 'runs.db')

    con = sqlite3.connect(db_run)
    cur = con.cursor()

    cur.execute(f'select filename from run order by savedAt desc')
    records = cur.fetchall()
    con.close()

    filenames = [record[0] for record in records]

    return filenames


def remove_run_by_filename(name):
    db_run = os.path.join(BADGER_DB_ROOT, 'runs.db')

    con = sqlite3.connect(db_run)
    cur = con.cursor()

    cur.execute(f'delete from run where filename = "{name}"')

    con.commit()
    con.close()


def remove_run_by_id(rid):
    db_run = os.path.join(BADGER_DB_ROOT, 'runs.db')

    con = sqlite3.connect(db_run)
    cur = con.cursor()

    cur.execute(f'delete from run where id = {rid}')

    con.commit()
    con.close()
