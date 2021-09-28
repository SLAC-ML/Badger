import sys
import os
import importlib
import yaml
import logging

BADGER_PLUGIN_ROOT = 'D:/Projects/Badger-Plugins'
sys.path.append(BADGER_PLUGIN_ROOT)


def scan_plugins(root):
    factory = {}
    for ptype in ['algorithm', 'interface', 'environment']:
        factory[ptype] = {}

        proot = os.path.join(root, f'{ptype}s')

        plugins = [fname for fname in os.listdir(proot)
                   if os.path.exists(os.path.join(proot, fname, '__init__.py'))]
        for pname in plugins:
            # TODO: Also load the configs here
            # So that list plugins can access the metadata of the plugins
            factory[ptype][pname] = None

    return factory


def load_plugin(root, pname, ptype):
    assert ptype in ['algorithm', 'interface',
                     'environment'], f'Invalid plugin type {ptype}'

    proot = os.path.join(root, f'{ptype}s')

    # Load the params in the configs
    configs = None
    with open(os.path.join(proot, pname, 'configs.yaml'), 'r') as f:
        try:
            configs = yaml.safe_load(f)
        except yaml.YAMLError:
            logging.error(
                f'Error loading plugin {ptype} {pname}: invalid config')

    # Load module
    module = importlib.import_module(f'{ptype}s.{pname}')

    if ptype == 'algorithm':
        plugin = [module.optimize, configs]
    elif ptype == 'interface':
        params = module.Interface.get_default_params()
        configs['params'] = params
        plugin = [module.Interface, configs]
    elif ptype == 'environment':
        vars = module.Environment.list_vars()
        obses = module.Environment.list_obses()
        params = module.Environment.get_default_params()
        configs['params'] = params
        configs['variables'] = vars
        configs['observations'] = obses
        plugin = [module.Environment, configs]

    BADGER_FACTORY[ptype][pname] = plugin

    return plugin


def get_plug(root, name, ptype):
    try:
        plug = BADGER_FACTORY[ptype][name]
        if plug is None:  # lazy loading
            plug = load_plugin(root, name, ptype)
            BADGER_FACTORY[ptype][name] = plug
    except KeyError:
        logging.error(
            f'Error loading plugin {ptype} {name}: plugin not found')
        plug = None

    return plug


def scan_extensions(root):
    extensions = {}

    eroot = os.path.join(root, 'extensions')

    enames = [fname for fname in os.listdir(eroot)
              if os.path.exists(os.path.join(eroot, fname, '__init__.py'))]
    for ename in enames:
        module = importlib.import_module(f'extensions.{ename}')
        ext = module.Extension()
        extensions[ename] = ext

    return extensions


def get_algo(name):
    if name in BADGER_FACTORY['algorithm'].keys():
        return get_plug(BADGER_PLUGIN_ROOT, name, 'algorithm')
    else:
        for ext in BADGER_EXTENSIONS.values():
            if name in ext.list_algo():
                return [ext, ext.get_algo_config(name)]


def get_intf(name):
    return get_plug(BADGER_PLUGIN_ROOT, name, 'interface')


def get_env(name):
    return get_plug(BADGER_PLUGIN_ROOT, name, 'environment')


def list_algo():
    algos = []
    algos += BADGER_FACTORY['algorithm']
    for ext in BADGER_EXTENSIONS.values():
        algos += ext.list_algo()
    return sorted(algos)


def list_intf():
    return sorted(BADGER_FACTORY['interface'])


def list_env():
    return sorted(BADGER_FACTORY['environment'])


BADGER_FACTORY = scan_plugins(BADGER_PLUGIN_ROOT)
BADGER_EXTENSIONS = scan_extensions(BADGER_PLUGIN_ROOT)
