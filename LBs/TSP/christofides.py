import numpy as np
import math
import time
from tqdm import tqdm
from instanceHandler import dynProgsTSP as dynProgs

def dynProgRelx(dynProgs):
    '''
    Christofides' State-Space Relaxation Procedure - |V|
    TODO: DFS scheme needed for "valid" state space reduction
    Returns a LB
    '''

    def getBound(memo,size,G,time_S):
        '''
        Makeshift validity check
        :param memo: dict for relaxed space
        :return: "valid" Lower bound
        '''

        path = {0:0}
        if size > 1 and memo.keys():
            for k in range(1,size):
                cost = np.inf
                for n in range(1,size):
                    if memo[(k,n)] < cost and n not in path.values():
                        path[k] = n
                        cost = memo[k,n]
            print("Took", math.ceil(time.time() - time_S), "seconds!!!")
        return cost+G[path[size-1],0],[path[i]+1 for i in range(size)]

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
    return getBound(memo,dynProgs.size,G,time_S)

instLb = dynProgs("a280")
lb = dynProgRelx(instLb)
print(instLb.name,":Lower Bound:",lb)