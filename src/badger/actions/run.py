from ..factory import get_algo, get_intf, get_env


def run_routine(args):
    Interface, configs_intf = get_intf('silly')
    Environment, configs_env = get_env('silly')
    optimize, configs_algo = get_algo('silly')

    params_algo = configs_algo['params'].copy()
    params_intf = configs_intf['params'].copy()
    params_env = configs_env['params'].copy()
    params_algo['dimension'] = 4
    params_algo['max_iter'] = 10
    params_intf['channel_count'] = 4
    params_env['dimension'] = 4

    intf = Interface(params_intf)
    env = Environment(intf, params_env)
    y_opt, x_opt = optimize(env.evaluate, params_algo)
    print(f'best! {x_opt}: {y_opt}')
