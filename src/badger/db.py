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


def load_routine(name):
    db_routine = os.path.join(BADGER_DB_ROOT, 'routines.db')
    con = sqlite3.connect(db_routine)
    cur = con.cursor()

    cur.execute('select * from routine where name=:name', {'name': name})
    records = cur.fetchall()
    con.close()

    if len(records) == 1:
        return yaml.safe_load(records[0][1]), records[0][2]
    elif len(records) == 0:
        logger.warn(f'Routine {name} not found in the database!')
        return None, None
    else:
        raise Exception(
            f'Multiple routines with name {name} found in the database!')


def list_routine():
    db_routine = os.path.join(BADGER_DB_ROOT, 'routines.db')
    con = sqlite3.connect(db_routine)
    cur = con.cursor()

    cur.execute('select name, savedAt from routine')
    records = cur.fetchall()
    names = [record[0] for record in records]
    timestamps = [record[1] for record in records]
    con.close()

    return names, timestamps


def save_run(run):
    pass


def load_run(name):
    pass
