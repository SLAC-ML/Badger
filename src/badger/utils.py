import os
import numpy as np
import yaml


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


def normalize_config_vars(config_vars):
    config = []
    for var in config_vars:
        if type(var) is dict:
            config.append(var)
        else:
            _var = {}
            _var[var] = [0, 1]
            config.append(_var)

    return config


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
                raise Exception(f'Error loading config {fname}: file not found')

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
        self.pareto_front = np.vstack((self.pareto_front[idx_keep], candidate[1]))
        self.pareto_set = np.vstack((self.pareto_set[idx_keep], candidate[0]))
        return False
