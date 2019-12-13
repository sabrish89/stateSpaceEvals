from random import sample
import numpy as np

def randomPath(tspInstance):
    '''
    Generate a random path, most likely suboptimal
    :param tspInstance: tsp instance
    :return: random cost
    '''

    path = sample(range(tspInstance.size),tspInstance.size)
    return sum([tspInstance.getCost()[path[i], path[(i+1)%tspInstance.size]] for i in range(tspInstance.size)])

def nearestNeighborPath(tspInstance):
    '''
    Generate a path using nearest neighbor heuristic (start somewhere (0) and always travel to next nearest vertex)
    Code from https://github.com/nschloe/tspsolve/blob/master/tspsolve/main.py
    :param tspInstance: tsp instance
    :return: greedy cost
    '''

    d = tspInstance.getCost()
    n = d.shape[0]
    idx = np.arange(n)
    path = np.empty(n, dtype=int)
    mask = np.ones(n, dtype=bool)

    last_idx = 0
    path[0] = last_idx
    mask[last_idx] = False
    for k in range(1, n):
        last_idx = idx[mask][np.argmin(d[last_idx, mask])]
        path[k] = last_idx
        mask[last_idx] = False
    return sum([tspInstance.getCost()[path[i], path[(i + 1) % tspInstance.size]] for i in range(tspInstance.size)])