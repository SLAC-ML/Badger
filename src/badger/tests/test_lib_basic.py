# def test_algo_api():
#     from badger.factory import get_algo

#     _, configs = get_algo('upper_confidence_bound')
#     assert configs['name'] == 'upper_confidence_bound'


def test_env_api():
    from badger.factory import list_env, get_env

    assert len(list_env()) == 2

    _, configs = get_env('test')
    assert configs['name'] == 'test'


def test_intf_api():
    from badger.factory import list_intf, get_intf

    assert len(list_intf()) == 1

    _, configs = get_intf('test')
    assert configs['name'] == 'test'


# def test_run(mock_config_root):
#     from coolname import generate_slug
#     from badger.log import config_log
#     config_log()
#     from badger.factory import get_algo, get_env
#     from badger.utils import load_config, merge_params, config_list_to_dict
#     from badger.core import normalize_routine, run_routine

#     # Args
#     algo = 'silly'
#     algo_params = '{dimension: 2, max_iter: 10}'
#     env = 'silly'
#     env_params = None
#     config = os.path.join(mock_config_root, 'test.yaml')
#     save = False
#     yes = True
#     verbose = 2

#     # Get env params
#     _, configs_env = get_env(env)

#     # Get algo params
#     _, configs_algo = get_algo(algo)

#     # Normalize the algo and env params
#     params_env = load_config(env_params)
#     params_algo = load_config(algo_params)
#     params_env = merge_params(configs_env['params'], params_env)
#     params_algo = merge_params(configs_algo['params'], params_algo)

#     # Load routine configs
#     configs_routine = load_config(config)

#     # Compose the routine
#     routine = {
#         'name': save or generate_slug(2),
#         'algo': algo,
#         'env': env,
#         'algo_params': params_algo,
#         'env_params': params_env,
#         # env_vranges is an additional info for the normalization
#         # Will be removed after the normalization
#         'env_vranges': config_list_to_dict(configs_env['variables']),
#         'config': configs_routine,
#     }

#     # Sanity check and config normalization
#     routine = normalize_routine(routine)

#     run_routine(routine, yes, save, verbose)
