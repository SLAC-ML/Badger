import requests
import os
from os.path import exists

def install_plugin(args): 

    current_path = os.getcwd()
    if not exists(f'{current_path}/.tmp'):
        os.mkdir('.tmp')
    
    full_path = f'{current_path}/.tmp'

    if args.install_1 is None:
        print('Please specify what you wish to install')
    
    url = ''
    arg = ''

    if args.install_2 is None: 
        url += f'http://localhost:3000/{args.install_1}'
        arg += args.install_1
                 
    elif args.install_1 == "algo": 
        url += f'http://localhost:3000/algorithms/{args.install_2}'
        arg += args.install_2
                    
    elif args.install_1 == "env": 
        url += f'http://localhost:3000/environments/{args.install_2}'
        arg += args.install_2

    else: 
        print('Please insert a valid argument')
        return
        
    r = requests.get(url)
    if r.status_code == 200:
        completePath = os.path.join(full_path, arg)
        with open(completePath, 'wb') as f:
            f.write(r.content)
    else: 
        print("A server with this url does not exist")

