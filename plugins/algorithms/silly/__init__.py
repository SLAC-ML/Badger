import numpy as np
from operator import itemgetter

def optimize(evaluate, params):
    D, max_iter = itemgetter('dimension', 'max_iter')(params)

    x_opt = None
    y_opt = np.Inf
    for i in range(max_iter):
        x = np.random.rand(D).reshape(1, -1)
        y = evaluate(x)
        print(f'yo! {x}: {y}')
        if y < y_opt:  # assume a minimize problem
            x_opt = x
            y_opt = y

    return y_opt, x_opt
