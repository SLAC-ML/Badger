from factory import get_algo, get_intf, get_env


Interface, params_intf = get_intf('silly')
Environment, params_env = get_env('silly')
optimize, params_algo = get_algo('silly')

params_algo['dimension'] = 4
params_algo['max_iter'] = 20
params_intf['channel_count'] = 4
params_env['dimension'] = 4

intf = Interface(params_intf)
env = Environment(intf, params_env)
y_opt, x_opt = optimize(env.evaluate, params_algo)
print(f'best! {x_opt}: {y_opt}')
