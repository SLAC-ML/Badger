import sys
import os
import importlib
import yaml
import logging

sys.path.append('D:/Projects/Badger-Plugins')


def scan_algorithms(root):
    factory_algo = {}

    algorithms = [fname for fname in os.listdir(root)
                  if os.path.exists(os.path.join(root, fname, '__init__.py'))]
    for algo in algorithms:
        module = importlib.import_module(f'algorithms.{algo}')
        # Load the params in the configs
        configs = None
        with open(os.path.join(root, algo, 'configs.yaml'), 'r') as f:
            try:
                configs = yaml.safe_load(f)
            except yaml.YAMLError:
                logging.error(
                    f'Error loading plugin algorithm {algo}: invalid config')
        if configs is None:
            params = None
        else:
            try:
                params = configs['params']
            except KeyError:
                params = None
        factory_algo[algo] = [module.optimize, params]

    return factory_algo


def scan_interfaces(root):
    factory_intf = {}

    interfaces = [fname for fname in os.listdir(root)
                  if os.path.exists(os.path.join(root, fname, '__init__.py'))]
    for intf in interfaces:
        module = importlib.import_module(f'interfaces.{intf}')
        # Load the params in the configs
        configs = None
        with open(os.path.join(root, intf, 'configs.yaml'), 'r') as f:
            try:
                configs = yaml.safe_load(f)
            except yaml.YAMLError:
                logging.error(
                    f'Error loading plugin interface {intf}: invalid config')
        if configs is None:
            params = None
        else:
            try:
                params = configs['params']
            except KeyError:
                params = None
        factory_intf[intf] = [module.Interface, params]

    return factory_intf


def scan_environments(root):
    factory_env = {}

    environments = [fname for fname in os.listdir(root)
                    if os.path.exists(os.path.join(root, fname, '__init__.py'))]
    for env in environments:
        module = importlib.import_module(f'environments.{env}')
        # Load the params in the configs
        configs = None
        with open(os.path.join(root, env, 'configs.yaml'), 'r') as f:
            try:
                configs = yaml.safe_load(f)
            except yaml.YAMLError:
                logging.error(
                    f'Error loading plugin environment {env}: invalid config')
        if configs is None:
            params = None
        else:
            try:
                params = configs['params']
            except KeyError:
                params = None
        factory_env[env] = [module.Environment, params]

    return factory_env


def scan_plugins():
    factory_algo = scan_algorithms('D:/Projects/Badger-Plugins/algorithms')
    factory_intf = scan_interfaces('D:/Projects/Badger-Plugins/interfaces')
    factory_env = scan_environments('D:/Projects/Badger-Plugins/environments')

    factory = {
        'algorithm': factory_algo,
        'interface': factory_intf,
        'environment': factory_env,
    }

    return factory


def get_algo(name):
    return BADGER_FACTORY['algorithm'][name]


def get_intf(name):
    return BADGER_FACTORY['interface'][name]


def get_env(name):
    return BADGER_FACTORY['environment'][name]


BADGER_FACTORY = scan_plugins()
