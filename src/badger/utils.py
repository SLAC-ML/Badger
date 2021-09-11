import os
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
            return configs
        except yaml.YAMLError:
            logging.error(
                f'Error parsing config {fname}: invalid yaml')
            return configs

    with open(fname, 'r') as f:
        try:
            configs = yaml.safe_load(f)
        except yaml.YAMLError:
            logging.error(
                f'Error loading config {fname}: invalid yaml')

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
