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
                    S = [x for x in list(range(1,N)) if x not in path[:-1]]
                    S.sort()
                    if S:
                        path.append(P[(tuple(S), path[-1])])
                    else:
                        path.insert(0,0)
            return [p+1 for p in path]

        time_S = time.time()
        memo = {}
        P = {}
        G = self.getCost()
        G = G + np.where(np.eye(self.size) > 0, np.inf, 0)
        for i in range(self.size):
            memo[(tuple({i}), i)] = G[0, i]
            P[(tuple({i}), i)] = 0
        for k in tqdm(range(2, self.size + 1)):
            if k < self.size:
                for aset in choiceGen(list(range(1,self.size)), k):
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
            else:
                aset = list(range(self.size))
                memo[tuple(aset), 0] = np.inf
                for u in range(len(aset)):
                    if u != 0:
                        S = list(set(aset).difference({0}))
                        S.sort()
                        z = memo[(tuple(S), aset[u])] + G[aset[u], 0]
                        if z < memo[(tuple(aset), 0)]:
                            memo[(tuple(aset), 0)] = z
                            P[(tuple(aset), 0)] = aset[u]
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

        def makePI(k,arrayNearestNeighbor):
            '''
            Get relaxed PI(p)\{i}
            '''
            candidates = set({})
            for i in range(k+1,len(arrayNearestNeighbor)):
                if candidates.__len__() > 0:
                    candidates = candidates.intersection(set(arrayNearestNeighbor[i]))
                else:
                    candidates = candidates.union(set(arrayNearestNeighbor[i]))
            return candidates

        def choiceGen(S, k):
            '''
            Get all subsets of set S of size k
            '''
            for x in combinations(S, k):
                yield x

        def functionEval(NG,k,i,memo,G):
            '''
            Recursor
            :param NG: NG relaxed path, set
            :param k: path length, int
            :param i: ender city, int
            '''

            if k > 1:
                return min([functionEval(NG.difference(i),k-1,j,memo,G) + G[i,j] for j in list(NG)])
            else:
                return G[NG[0],i]

        time_S = time.time()
        memo = {}
        G = self.getCost()
        G = G + np.where(np.eye(self.size) > 0, np.inf, 0)
        N = nearestNeighbors(self)
        NG = set(range(self.size))
        for i in range(self.size):
            memo[(NG,self.size,i)] = sum(functionEval(NG,self.size,i,memo,G))
        print(memo)


inst = dynProgs("ulysses22")
G = inst.getCost()
print(inst.dynProgSol())