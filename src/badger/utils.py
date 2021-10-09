import os
import numpy as np
import yaml
import logging


# https://stackoverflow.com/a/39681672/4263605
# https://github.com/yaml/pyyaml/issues/234#issuecomment-765894586
class Dumper(yaml.Dumper):

    def increase_indent(self, flow=False, indentless=False):
        return super(Dumper, self).increase_indent(flow, False)


def yprint(content):
    print(yaml.dump(content, Dumper=Dumper,
          default_flow_style=False, sort_keys=False), end='')


def norm(x, lb, ub):
    return (x - lb) / (ub - lb)


def denorm(x, lb, ub):
    return (1 - x) * lb + x * ub


def config_list_to_dict(config_list):
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


def normalize_routine(routine):
    # Sanity check and config normalization
    #
    # routine
    #  name
    #  algo
    #  env
    #  algo_params
    #  env_params
    #  env_vranges: use for vars normalization in config
    #  config: change the var ranges, the obj rules, and the constraints
    env_vranges = routine['env_vranges']
    config = routine['config']

    # Normalize the variables
    for i, var in enumerate(config['variables']):
        if type(var) is str:
            config['variables'][i] = _dict = {}
            _dict[var] = env_vranges[var]
        else:
            var_name = next(iter(var))  # get the only (first) key in the dict
            vrange_vocs = var[var_name]
            vrange_default = env_vranges[var_name]

            if vrange_vocs is None:
                var[var_name] = vrange_default
                continue

            if vrange_vocs[0] < vrange_default[0]:
                logging.warn(
                    f'variable {var_name}: lower limit {vrange_vocs[0]} exceeds the bound, set to the lower bound {vrange_default[0]}')
                lb = vrange_default[0]
            else:
                lb = vrange_vocs[0]
            if vrange_vocs[1] > vrange_default[1]:
                logging.warn(
                    f'variable {var_name}: upper limit {vrange_vocs[1]} exceeds the bound, set to the upper bound {vrange_default[1]}')
                ub = vrange_default[1]
            else:
                ub = vrange_vocs[1]

            if lb >= ub:  # TODO: add logic to deal with the == condition
                raise Exception(
                    f'variable {var_name}: lower limit {lb} must be lower than the upper limit {ub}!')
            var[var_name] = [lb, ub]

    # Normalize the objectives
    for i, obj in enumerate(config['objectives']):
        if type(obj) is str:
            config['objectives'][i] = _dict = {}
            _dict[obj] = 'MINIMIZE'
        else:
            obj_name = next(iter(obj))
            if obj[obj_name] is None:
                obj[obj_name] = 'MINIMIZE'

    # TODO: Normalize the constraints

    # Remove the additional info
    del routine['env_vranges']

    return routine


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
