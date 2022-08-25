import shutil
from os.path import exists
try:
    from ..factory import BADGER_PLUGIN_ROOT
except:
    BADGER_PLUGIN_ROOT = None

hist = {'algo': 'algorithms',
        'env' : 'environments',
        'ext' : 'extensions',
        'int' : 'interfaces'}

def plugin_remove(args): 
	if args.plugin_type is None or args.plugin_specific is None: 
		print('Please specify further which plugin you wish to remove!')
		return 
	try: 
		full_word = hist[f'{args.plugin_type}']
	except KeyError:
		print(f'{args.plugin_type} is not an existing plugin type') 

	plugin_path = f'{BADGER_PLUGIN_ROOT}/{full_word}/{args.plugin_specific}'
	if not exists(plugin_path): 
		print(f'The plugin {args.plugin_specific} already does not exist!')
		return
	try:
		shutil.rmtree(plugin_path)
	except OSError as e:
		print(f'Error: {plugin_path} : {e.strerror}')
	else: 
		print(f'{args.plugin_specific} was removed successfully from {BADGER_PLUGIN_ROOT}/{full_word}')
		print(f'NOTE: The plugin dependencies for {args.plugin_specific} have not been removed')

	


