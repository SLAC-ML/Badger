import sys
import os
import importlib
import yaml
import logging

# Check badger plugin root
BADGER_PLUGIN_ROOT = os.getenv('BADGER_PLUGIN_ROOT')
if BADGER_PLUGIN_ROOT is None:
    logging.error('Please set the BADGER_PLUGIN_ROOT env var!')
    sys.exit()
elif not os.path.exists(BADGER_PLUGIN_ROOT):
    logging.error(
        f'The badger plugin root {BADGER_PLUGIN_ROOT} does not exist!')
    sys.exit()
else:
    module_file = os.path.join(BADGER_PLUGIN_ROOT, '__init__.py')
    if not os.path.exists(module_file):
        with open(module_file, 'w') as f:
            pass
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
            return [None, None]

    # Load module
    try:
        module = importlib.import_module(f'{ptype}s.{pname}')
    except ImportError as e:
        logging.error(
            f'{ptype} {pname} is not available due to missing dependencies: {e}')
        return [None, configs]

    if ptype == 'algorithm':
        plugin = [module.optimize, configs]
    elif ptype == 'interface':
        params = module.Interface.get_default_params()
        configs['params'] = params
        plugin = [module.Interface, configs]
    elif ptype == 'environment':
        vars = module.Environment.list_vars()
        vranges = module.Environment.get_vranges()
        obses = module.Environment.list_obses()
        params = module.Environment.get_default_params()

        vars_info = []
        for i, var in enumerate(vars):
            var_info = {}
            var_info[var] = vranges[i]
            vars_info.append(var_info)

        configs['params'] = params
        configs['variables'] = vars_info
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
        # Prevent accidentially modifying default configs
        plug = [plug[0], plug[1].copy()]
    except KeyError:
        logging.error(
            f'Error loading plugin {ptype} {name}: plugin not found')
        plug = [None, None]

    return plug


def scan_extensions(root):
    extensions = {}

    eroot = os.path.join(root, 'extensions')

    enames = [fname for fname in os.listdir(eroot)
              if os.path.exists(os.path.join(eroot, fname, '__init__.py'))]
    for ename in enames:
        try:
            module = importlib.import_module(f'extensions.{ename}')
            ext = module.Extension()
            extensions[ename] = ext
        except ImportError:
            pass
            # logging.warn(
            #     f'Extension {ename} is not available due to missing dependencies')

    return extensions


def get_algo(name):
    if name in BADGER_FACTORY['algorithm'].keys():
        return get_plug(BADGER_PLUGIN_ROOT, name, 'algorithm')
    else:
        for ext in BADGER_EXTENSIONS.values():
            if name in ext.list_algo():
                return [ext, ext.get_algo_config(name)]

        logging.error(
            f'Error loading plugin algorithm {name}: plugin not found')
        return [None, None]


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
