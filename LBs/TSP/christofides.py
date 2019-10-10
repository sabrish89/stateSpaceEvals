import numpy as np
from itertools import combinations
import math
import time
from tqdm import tqdm
from dynamicProgramming.dynProg import dynProgs
from tsplibInstanceReader import produce_matrix

def dynProgRelx(dynProgs):
    '''
    Christofides' State-Space Relaxation Procedure - |V|
    bottom-up recursion
    Returns a LB
    '''

    time_S = time.time()
    memo = {}
    G = dynProgs.getCost()
    G = G + np.where(np.eye(dynProgs.size) > 0, np.inf, 0)
    for i in range(dynProgs.size):
        memo[(1, i)] = G[0, i]
    for k in tqdm(range(2, dynProgs.size)):
        for w in range(1, dynProgs.size):
            memo[(k, w)] = np.inf
            for u in range(1, dynProgs.size):
                if u != w:
                    z = memo[(k - 1, u)] + G[u, w]
                    if z < memo[(k, w)]:
                        memo[(k, w)] = z
    print("Took", math.ceil(time.time() - time_S), "seconds!!!")
    return max([memo[(dynProgs.size - 1, i)] + G[i, 0] for i in range(1, dynProgs.size)])

inst = dynProgs("kroA150")
G = inst.getCost()
lb = dynProgRelx(inst)
print("Lower Bound:",lb)