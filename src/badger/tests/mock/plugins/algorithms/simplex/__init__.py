import numpy as np
import scipy.optimize as sopt
from operator import itemgetter
import logging


def optimize(evaluate, params):
    D, x0, isteps, xtol, max_iter = \
        itemgetter('dimension', 'x0', 'isteps', 'xtol', 'max_iter')(params)

    assert len(x0) == D, 'Dimension does not match!'

    if isteps is None or len(isteps) != D:
        logging.warning("Initial simplex is None")
        isim = None
    elif np.count_nonzero(isteps) != D:
        logging.warning("There is zero step. Initial simplex is None")
        isim = None
    else:
        isim = np.zeros((D + 1, D))
        isim[0] = x0
        for i in range(D):
            vertex = np.zeros(D)
            vertex[i] = isteps[i]
            isim[i + 1] = x0 + vertex

    logging.debug(f'ISIM = {isim}')

    def _evaluate(x):
        y, _, _, _ = evaluate(np.array(x).reshape(1, -1))
        y = y[0]

        return y

    res = sopt.fmin(_evaluate, x0, maxiter=max_iter,
                    maxfun=max_iter, xtol=xtol, initial_simplex=isim)

    return res
