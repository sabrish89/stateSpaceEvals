import numpy as np
from itertools import combinations
import math
import time
from tqdm import tqdm
from tsplibInstanceReader import produce_matrix

class dynProgs(object):

    def __init__(self,instance_name):
        '''
        produce an instance with the data for cost matrix
        '''

        self.name = instance_name
        self.size = 0

    def getCost(self):
        '''
        getter for cost
        :return: cost matrix
        '''

        costMatrix = produce_matrix(self.name)
        self.size = costMatrix.shape[0]
        return costMatrix

    def dynProgSol(self):
        '''
        prohibitive complexity ~ O(n^2 * 2^n)
        A memoized state-space search using DP
        TODO: can use tf?
        :return: path and cost
        '''

        def choiceGen(S, k):
            '''
            Get all subsets of set S of size k
            '''
            for x in combinations(S, k):
                yield x

        def pathGen(P, N):
            '''
            Get path from DP solution
            '''
            path = []
            while path.__len__() < N + 1:
                if path.__len__() == 0:
                    path.append(P[(tuple(list(range(N))), 0)])
                else:
                    S = [x for x in list(range(N)) if x not in path[:-1]]
                    S.sort()
                    path.append(P[(tuple(S), path[-1])])
            path.remove(0)
            return [p + 1 for p in path]

        time_S = time.time()
        memo = {}
        P = {}
        G = self.getCost()
        G = G + np.where(np.eye(self.size) > 0, np.inf, 0)
        for i in range(self.size):
            memo[(tuple({i}), i)] = G[0, i]
            P[(tuple({i}), i)] = 0
        for k in tqdm(range(2, self.size + 1)):
            for aset in choiceGen(list(range(self.size)), k):
                for w in range(len(aset)):
                    memo[tuple(aset), aset[w]] = np.inf
                    for u in range(len(aset)):
                        if u != w:
                            S = list(set(aset).difference({aset[w]}))
                            S.sort()
                            z = memo[(tuple(S), aset[u])] + G[aset[u], aset[w]]
                            if z < memo[(tuple(aset), aset[w])]:
                                memo[(tuple(aset), aset[w])] = z
                                P[(tuple(aset), aset[w])] = aset[u]
        print("Took", math.ceil(time.time() - time_S), "seconds!!!")
        return memo[(tuple(list(range(self.size))), 0)], pathGen(P, self.size)

    def dynProgWithDng(self,delta=6):
        '''
        Dng-relaxed state space
        Paper requires delta = 8,10 for relaxation to be tight
        '''

        def nearestNeighbors(self,d=delta):
            '''
            ~ n^2 * log(n)
            '''
            C = self.getCost()
            return [np.argsort(C[i]).tolist()[:d+1] for i in range(C.shape[0])]

        def smallestSubtour(tour):
            '''
            returns smallest subtour found with start,end indices and vertex
            :param tour: list
            :return: dic {i:[start,end]}, -1
            TODO: Linear, optimizable?
            '''
            dickt = {}
            mark = [None,np.inf]
            for i in range(tour.__len__()):
                if tour[i] not in dickt.keys():
                    dickt[tour[i]] = [i]
                else:
                    dickt[tour[i]].append(i)
                    if dickt[tour[i]][1] - dickt[tour[i]][0] < mark[1]:
                        mark[0] = i
            return dickt[mark[0]] if mark[0] else None

        def makePI(lp,k,arrayNearestNeighbor):
            '''
            Get relaxed PI(p)
            '''
            candidates = set({})
            for i in range(k+1,len(arrayNearestNeighbor)):
                if candidates.__len__() > 0:
                    candidates.intersection(arrayNearestNeighbor[i])
                else:
                    candidates.union(arrayNearestNeighbor[i])
            return candidates.union(lp)

        time_S = time.time()
        memo = {}
        P = {}
        G = self.getCost()
        G = G + np.where(np.eye(self.size) > 0, np.inf, 0)
        N = nearestNeighbors(self)
        for i in range(self.size):
            memo[(tuple({i}), i)] = G[0, i]
            P[(tuple({i}), i)] = 0
        for k in tqdm(range(2, self.size + 1)):
            for end in range(self.size):
                if u != w:
                    S = list(set(aset).difference({aset[w]}))
                    S.sort()
                    z = memo[(tuple(S), aset[u])] + G[aset[u], aset[w]]
                    if z < memo[(tuple(aset), aset[w])]:
                        memo[(tuple(aset), aset[w])] = z
                        P[(tuple(aset), aset[w])] = aset[u]



inst = dynProgs("burma14")

G = inst.getCost()
cost,path = inst.dynProgSol()
print(cost,path)