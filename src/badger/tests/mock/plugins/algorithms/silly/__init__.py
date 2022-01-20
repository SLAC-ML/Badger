import numpy as np
from operator import itemgetter
from badger.utils import ParetoFront


def optimize(evaluate, params):
    D, max_iter = itemgetter('dimension', 'max_iter')(params)

    for i in range(max_iter):
        x = np.random.rand(D).reshape(1, -1)
        y, _, _, _ = evaluate(x)
        if not i:
            pf = ParetoFront(['MINIMIZE'] * y.shape[1])

        pf.is_dominated((x, y))
    # print(len(pf.pareto_front) / max_iter)

    return pf.pareto_front, pf.pareto_set
