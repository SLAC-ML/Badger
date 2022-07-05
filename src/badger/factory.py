from .settings import read_value
import sys
import os
import importlib
import yaml
import logging
logger = logging.getLogger(__name__)


# Check badger plugin root
BADGER_PLUGIN_ROOT = read_value('BADGER_PLUGIN_ROOT')
if BADGER_PLUGIN_ROOT is None:
    raise Exception('Please set the BADGER_PLUGIN_ROOT env var!')
elif not os.path.exists(BADGER_PLUGIN_ROOT):
    raise Exception(
        f'The badger plugin root {BADGER_PLUGIN_ROOT} does not exist!')
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

        try:
            plugins = [fname for fname in os.listdir(proot)
                       if os.path.exists(os.path.join(proot, fname, '__init__.py'))]
        except:
            plugins = []

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
            raise Exception(
                f'Error loading plugin {ptype} {pname}: invalid config')

    # Load module
    try:
        module = importlib.import_module(f'{ptype}s.{pname}')
    except ImportError as e:
        _e = Exception(
            f'{ptype} {pname} is not available due to missing dependencies: {e}')
        _e.configs = configs  # attach information to the exception
        raise _e

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
        # Get vranges by creating an env instance
        try:
            intf_name = configs['interface'][0]
            Interface, _ = get_intf(intf_name)
            intf = Interface()
        except KeyError:
            intf = None
        except Exception as e:
            logger.warning(e)
            intf = None
        env = module.Environment(intf, configs)
        vranges = env.get_vranges()

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
        raise Exception(
            f'Error loading plugin {ptype} {name}: plugin not found')

    return plug


def scan_extensions(root):
    extensions = {}

    eroot = os.path.join(root, 'extensions')

    try:
        enames = [fname for fname in os.listdir(eroot)
                  if os.path.exists(os.path.join(eroot, fname, '__init__.py'))]
    except:
        enames = []

    for ename in enames:
        try:
            module = importlib.import_module(f'extensions.{ename}')
            ext = module.Extension()
            extensions[ename] = ext
        except ImportError:  # usually caused by missing dependencies
            logger.debug(
                f'Extension {ename} is not available due to missing dependencies')
        except Exception as e:
            logger.debug(
                f'Failed to load extension {ename}: {str(e)}')

    return extensions


def get_algo(name):
    if name in BADGER_FACTORY['algorithm'].keys():
        return get_plug(BADGER_PLUGIN_ROOT, name, 'algorithm')
    else:
        for ext_name in BADGER_EXTENSIONS.keys():
            ext = BADGER_EXTENSIONS[ext_name]
            try:
                if name in ext.list_algo():
                    return [ext, ext.get_algo_config(name)]
            except ImportError as e:
                logger.warning(
                    f'Failed to read algorithms from ext {ext_name}: {str(e)}')

        raise Exception(
            f'Error loading plugin algorithm {name}: plugin not found')


def get_intf(name):
    return get_plug(BADGER_PLUGIN_ROOT, name, 'interface')


def get_env(name):
    return get_plug(BADGER_PLUGIN_ROOT, name, 'environment')


def list_algo():
    algos = []
    algos += BADGER_FACTORY['algorithm']
    for ext_name in BADGER_EXTENSIONS.keys():
        ext = BADGER_EXTENSIONS[ext_name]
        try:
            algos += ext.list_algo()
        except ImportError as e:
            logger.warning(
                f'Failed to list algorithms from ext {ext_name}: {str(e)}')
    return sorted(algos)


def list_intf():
    return sorted(BADGER_FACTORY['interface'])


def list_env():
    return sorted(BADGER_FACTORY['environment'])


BADGER_FACTORY = scan_plugins(BADGER_PLUGIN_ROOT)
BADGER_EXTENSIONS = scan_extensions(BADGER_PLUGIN_ROOT)
