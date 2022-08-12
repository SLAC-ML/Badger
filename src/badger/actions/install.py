import requests
import tarfile
import json
import os
from os.path import exists
try:
    from ..factory import BADGER_PLUGIN_ROOT
except:
    BADGER_PLUGIN_ROOT = None

# !!!!!!!!  Need prep for port not being 3000 

current_path = os.getcwd()
if not exists(f'{current_path}/.tmp'):
    os.mkdir('.tmp')
tmp_path = f'{current_path}/.tmp'

hist = {'algo': 'algorithms',
        'env' : 'environments',
        'ext' : 'extensions',
        'int' : 'interfaces'}


def plugin_install(args): 
    if args.plugin_type is None: 
        print("Please specify further what you wish to install!")
        return

    full_word = hist[f'{args.plugin_type}']

    if args.plugin_specific is None: 
        url = f'http://localhost:3000/api/{full_word}'
        r = requests.get(url)
        for elem in r.json():
            if exists(f'{BADGER_PLUGIN_ROOT}/{full_word}/{elem}'): 
                print(elem, '  (Already installed)')
            else:
                print(elem)
        return

    targz_path = os.path.join(tmp_path, f'{args.plugin_specific}.tar.gz')

    r_d = requests.get(f'http://localhost:3000/api/url/{args.plugin_specific}')
    download_url = r_d.text

    r = requests.get(download_url)
    if r.status_code == 200:
        with open(targz_path, 'wb') as f:
            f.write(r.content)
        os.chdir(tmp_path)
        tar = tarfile.open(f'{args.plugin_specific}.tar.gz', 'r:gz')  
        plugin_path = f'{BADGER_PLUGIN_ROOT}/{full_word}/{args.plugin_specific}'
        if exists(plugin_path): 
            print('This plugin is already installed!')
            return
        tar.extractall(f'{BADGER_PLUGIN_ROOT}/{full_word}')
        tar.close()
    else: 
        print("The server does not have this plugin!")
        return









    


