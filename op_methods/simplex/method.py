import numpy as np
import scipy as sp
from operator import itemgetter
import logging

def optimize(evaluate, params):
    D, x0, dev_steps, xtol, max_iter = \
        itemgetter('dimension', 'x0', 'dev_steps', 'xtol', 'max_iter')(params)

    assert len(x0) == D, 'Dimension does not match!'

    if dev_steps is None or len(dev_steps) != D:
        logging.warn("Initial simplex is None")
        isim = None
    elif np.count_nonzero(dev_steps) != D:
        logging.warn("There is zero step. Initial simplex is None")
        isim = None
    else:
        isim = np.zeros((D + 1, D))
        isim[0] = x0
        for i in range(D):
            vertex = np.zeros(D)
            vertex[i] = dev_steps[i]
            isim[i + 1] = x0 + vertex

    logging.debug(f'ISIM = {isim}')

    res = sp.optimize.fmin(evaluate, x0, maxiter=max_iter,
        maxfun=max_iter, xtol=xtol, initial_simplex=isim)

    return res
