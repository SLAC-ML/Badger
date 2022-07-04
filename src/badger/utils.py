import os
from datetime import datetime
import numpy as np
import yaml


# https://stackoverflow.com/a/39681672/4263605
# https://github.com/yaml/pyyaml/issues/234#issuecomment-765894586
class Dumper(yaml.Dumper):

    def increase_indent(self, flow=False, indentless=False):
        return super(Dumper, self).increase_indent(flow, False)


def ystring(content):
    if content is None:
        return ''

    return yaml.dump(content, Dumper=Dumper, default_flow_style=False, sort_keys=False)


def yprint(content):
    print(ystring(content), end='')


def norm(x, lb, ub):
    return (x - lb) / (ub - lb)


def denorm(x, lb, ub):
    return (1 - x) * lb + x * ub


def config_list_to_dict(config_list):
    if not config_list:
        return {}

    book = {}
    for config in config_list:
        for k, v in config.items():
            book[k] = v

    return book


def load_config(fname):
    configs = None

    if fname is None:
        return configs

    # if fname is a yaml string
    if not os.path.exists(fname):
        try:
            configs = yaml.safe_load(fname)
            # A string is also a valid yaml
            if type(configs) is str:
                raise Exception(
                    f'Error loading config {fname}: file not found')

            return configs
        except yaml.YAMLError:
            raise Exception(f'Error parsing config {fname}: invalid yaml')

    with open(fname, 'r') as f:
        try:
            configs = yaml.safe_load(f)
        except yaml.YAMLError:
            raise Exception(f'Error loading config {fname}: invalid yaml')

    return configs


def merge_params(default_params, params):
    merged_params = None

    if params is None:
        merged_params = default_params
    elif default_params is None:
        merged_params = params
    else:
        merged_params = {**default_params, **params}

    return merged_params


def range_to_str(vranges):
    # Transfer the range list to a string for better printing
    vranges_str = []
    for var_dict in vranges:
        var = next(iter(var_dict))
        vrange = var_dict[var]
        vranges_str.append({})
        vranges_str[-1][var] = f'{vrange[0]} -> {vrange[1]}'

    return vranges_str


class ParetoFront:

    def __init__(self, rules):
        # rules: ['MAXIMIZE', 'MINIMIZE', ...]
        self.rules = (np.array(rules) == 'MINIMIZE') * 2 - 1
        self.dimension = len(rules)
        self.pareto_set = None
        self.pareto_front = None

    def is_dominated(self, candidate):
        # candidate: (x: array-like, y: array-like)
        # First candidate
        if self.pareto_front is None:
            self.pareto_set = np.array(candidate[0]).reshape(1, -1)
            self.pareto_front = np.array(candidate[1]).reshape(1, -1)
            return False

        dmat = (self.pareto_front - candidate[1]) * self.rules > 0
        scores = np.sum(dmat, axis=1)
        if np.sum(scores == 0):  # candidate is dominated
            return True

        # Drop points that are dominated by candidate
        idx_keep = (scores != self.dimension)
        self.pareto_front = np.vstack(
            (self.pareto_front[idx_keep], candidate[1]))
        self.pareto_set = np.vstack((self.pareto_set[idx_keep], candidate[0]))
        return False


def ts_to_str(ts, format='lcls-log'):
    if format == 'lcls-log':
        return ts.strftime('%d-%b-%Y %H:%M:%S')
    elif format == 'lcls-log-full':
        return ts.strftime('%d-%b-%Y %H:%M:%S.%f')
    elif format == 'lcls-fname':
        return ts.strftime('%Y-%m-%d-%H%M%S')
    else:  # ISO format
        return ts.isoformat()


def str_to_ts(timestr, format='lcls-log'):
    if format == 'lcls-log':
        return datetime.strptime(timestr, '%d-%b-%Y %H:%M:%S')
    elif format == 'lcls-log-full':
        return datetime.strptime(timestr, '%d-%b-%Y %H:%M:%S.%f')
    elif format == 'lcls-fname':
        return datetime.strptime(timestr, '%Y-%m-%d-%H%M%S')
    else:  # ISO format
        return datetime.fromisoformat(timestr)


def curr_ts():
    return datetime.now()


def curr_ts_to_str(format='lcls-log'):
    return ts_to_str(datetime.now(), format)


def get_header(routine):
    try:
        obj_names = [next(iter(d))
                        for d in routine['config']['objectives']]
    except:
        obj_names = []
    try:
        var_names = [next(iter(d))
                        for d in routine['config']['variables']]
    except:
        var_names = []
    try:
        if routine['config']['constraints']:
            con_names = [next(iter(d))
                            for d in routine['config']['constraints']]
        else:
            con_names = []
    except:
        con_names = []
    try:
        sta_names = routine['config']['states'] or []
    except KeyError:
        sta_names = []

    return obj_names + con_names + var_names + sta_names


def run_names_to_dict(run_names):
    runs = {}
    for name in run_names:
        tokens = name.split('-')
        year = tokens[1]
        month = tokens[2]
        day = tokens[3]

        try:
            year_dict = runs[year]
        except:
            runs[year] = {}
            year_dict = runs[year]
        key_month = f'{year}-{month}'
        try:
            month_dict = year_dict[key_month]
        except:
            year_dict[key_month] = {}
            month_dict = year_dict[key_month]
        key_day = f'{year}-{month}-{day}'
        try:
            day_list = month_dict[key_day]
        except:
            month_dict[key_day] = []
            day_list = month_dict[key_day]
        day_list.append(name)

    return runs
