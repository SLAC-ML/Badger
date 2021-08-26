from .factory import get_algo, get_intf, get_env


def main(args=None):
    Interface, params_intf = get_intf('silly')
    Environment, params_env = get_env('silly')
    optimize, params_algo = get_algo('silly')

    params_algo['dimension'] = 3
    params_algo['max_iter'] = 10
    params_intf['channel_count'] = 3
    params_env['dimension'] = 3

    intf = Interface(params_intf)
    env = Environment(intf, params_env)
    y_opt, x_opt = optimize(env.evaluate, params_algo)
    print(f'best! {x_opt}: {y_opt}')


if __name__ == '__main__':
    main()
