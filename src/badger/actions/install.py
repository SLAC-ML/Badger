import requests
import tarfile
import json
import os
import yaml
import conda.cli
from tqdm.auto import tqdm
from conda.cli.python_api import run_command, Commands
import shutil
from os.path import exists
from ..settings import list_settings, BADGER_CORE_DICT
try:
    from ..factory import BADGER_PLUGIN_ROOT
except:
    BADGER_PLUGIN_ROOT = None


current_path = os.getcwd()
if not exists(f'{current_path}/.tmp'):
    os.mkdir('.tmp')
tmp_path = f'{current_path}/.tmp'

hist = {'algo': 'algorithms',
        'env' : 'environments',
        'ext' : 'extensions',
        'int' : 'interfaces'}

identify = {'optimize'    :  'algorithms', 
            'Environment' :  'environments', 
            'Extension'   :  'extensions', 
            'Interface'   :  'interfaces'}
    

plugins_url = BADGER_CORE_DICT['BADGER_PLUGINS_URL']['default value']
# plugins_url = 'http://localhost:3000'

def plugin_install(args): 
    plugin_path = ''
    if args.plugin_type is None: 
        print("Please specify further what you wish to install!")
        return

    if args.plugin_type != 'local' and args.plugin_type not in hist: 
        print(f"{args.plugin_type} is an invalid option. Choose one of the following:  algo, env, ext, int, local")
        return

    if args.plugin_specific is None: 
        if args.plugin_type == 'local': 
            print('Please specify further what plugin you wish to install')
            return
        url = f'{plugins_url}/api/{full_word}'     
        r = requests.get(url)
        for elem in r.json():
            if exists(f'{BADGER_PLUGIN_ROOT}/{full_word}/{elem}'): 
                print(elem, '         (Already installed)')
            else:
                print(elem)
        return

    if args.plugin_type == 'local': 
        tarname = os.path.basename(os.path.normpath(args.plugin_specific))
        plugin_name = tarname[:-7]
        local_path = os.path.dirname(args.plugin_specific)
        os.chdir(local_path)
        tar = tarfile.open(f'{tarname}', 'r:gz') 
        tar.extractall(tmp_path)
        tar.close()

        histog = {}
        os.chdir(f'{tmp_path}/{plugin_name}')
        with open('__init__.py', 'r') as file:
            info = file.read()
        exec(info, histog)
        identifier = list(histog.keys())[-1]
        full_word = identify[identifier]
        plugin_path += f'{BADGER_PLUGIN_ROOT}/{full_word}/{plugin_name}'
        if exists(plugin_path): 
            print('This plugin is already installed!')
            return
        shutil.move(f'{tmp_path}/{plugin_name}', f'{BADGER_PLUGIN_ROOT}/{full_word}')  
        shutil.rmtree(tmp_path)
        
        
    else: 
        full_word = hist[f'{args.plugin_type}']
        targz_path = os.path.join(tmp_path, f'{args.plugin_specific}.tar.gz')

        r_d = requests.get(f'{plugins_url}/api/url/{full_word}/{args.plugin_specific}')     
        download_url = r_d.text

        r = requests.get(download_url)
        if r.status_code == 200:
            with open(targz_path, 'wb') as f:
                f.write(r.content)
            os.chdir(tmp_path)
            tar = tarfile.open(f'{args.plugin_specific}.tar.gz', 'r:gz')  
            plugin_path += f'{BADGER_PLUGIN_ROOT}/{full_word}/{args.plugin_specific}'
            if exists(plugin_path): 
                print('This plugin is already installed!')
                return
            print(f'Installing {args.plugin_specific} into {BADGER_PLUGIN_ROOT}/{full_word} ...')
            tar.extractall(f'{BADGER_PLUGIN_ROOT}/{full_word}')
            tar.close()
        else: 
            print("The server does not have this plugin!")
            return

    os.chdir(plugin_path)
    with open("configs.yaml", "r") as stream:
        try:
            configs = yaml.safe_load(stream)
        except yaml.YAMLError as e:
            print(e)
        else: 
            dependencies = configs['dependencies']
            print('Installing plugin dependencies ...')
            try: 
                dependencies.remove('badger-opt')
            except ValueError: 
                pass
            for elem in tqdm(dependencies): 
                stdout_str, stderr_str, return_code_int = run_command(Commands.INSTALL, ["-y", f'{elem}'])
                if return_code_int != 0:
                    shutil.rmtree(plugin_path)
                    print(stderr_str)
            print('All dependencies successfully installed!')
            print('Plugin installation complete!')



