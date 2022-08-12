import requests
import json
import os
from os.path import exists

# !!!!!!!!  Need prep for port not being 3000 

current_path = os.getcwd()
if not exists(f'{current_path}/.tmp'):
    os.mkdir('.tmp')
full_path = f'{current_path}/.tmp'


def install_only(args): 
    print("Please specify further what you wish to install!")
    


def install_algo(args):
    if args.algo_plugin is None:
        url = 'http://localhost:3000/api/algorithms'
        r = requests.get(url)
        for elem in r.json():
            if exists(os.path.join(full_path, f'{elem}.tar.gz')): 
                print(elem, '  (Already installed)')
            else:
                print(elem)
        return

    completePath = os.path.join(full_path, f'{args.algo_plugin}.tar.gz')
    r_d = requests.get(f'http://localhost:3000/api/url/{args.algo_plugin}')
    download_url = r_d.text

    r = requests.get(download_url)
    if r.status_code == 200:
         if exists(completePath): 
            print('This algorithm plugin is already installed!')
            return
         with open(completePath, 'wb') as f:
             f.write(r.content)
    else: 
        print("A server with this url does not exist")
        return



def install_env(args):
    if args.env_plugin is None:
        url = 'http://localhost:3000/api/environments'
        r = requests.get(url)
        for elem in r.json():
            if exists(os.path.join(full_path, f'{elem}.tar.gz')): 
                print(elem, '  (Already installed)')
            else:
                print(elem)
        return

    completePath = os.path.join(full_path, f'{args.env_plugin}.tar.gz')
    r_d = requests.get(f'http://localhost:3000/api/url/{args.env_plugin}')
    download_url = r_d.text

    r = requests.get(download_url)
    if r.status_code == 200:
         if exists(completePath): 
            print('This environment plugin is already installed!')
            return
         with open(completePath, 'wb') as f:
             f.write(r.content)
    else: 
        print("A server with this url does not exist")
        return



def install_ext(args):
    if args.ext_plugin is None:
        url = 'http://localhost:3000/api/extensions'
        r = requests.get(url)
        for elem in r.json():
            if exists(os.path.join(full_path, f'{elem}.tar.gz')): 
                print(elem, '  (Already installed)')
            else:
                print(elem)
        return

    completePath = os.path.join(full_path, f'{args.ext_plugin}.tar.gz')
    r_d = requests.get(f'http://localhost:3000/api/url/{args.ext_plugin}')
    download_url = r_d.text

    r = requests.get(download_url)
    if r.status_code == 200:
         if exists(completePath): 
            print('This extension plugin is already installed!')
            return
         with open(completePath, 'wb') as f:
             f.write(r.content)
    else: 
        print("A server with this url does not exist")
        return



def install_int(args):
    if args.int_plugin is None:
        url = 'http://localhost:3000/api/interfaces'
        r = requests.get(url)
        for elem in r.json():
            if exists(os.path.join(full_path, f'{elem}.tar.gz')): 
                print(elem, '  (Already installed)')
            else:
                print(elem)
        return

    completePath = os.path.join(full_path, f'{args.int_plugin}.tar.gz')
    r_d = requests.get(f'http://localhost:3000/api/url/{args.int_plugin}')
    download_url = r_d.text

    r = requests.get(download_url)
    if r.status_code == 200:
         if exists(completePath): 
            print('This interfaces plugin is already installed!')
            return
         with open(completePath, 'wb') as f:
             f.write(r.content)
    else: 
        print("A server with this url does not exist")
        return
    








    


