import numpy as np
from itertools import combinations
import math
import time
from tqdm import tqdm
from instanceHandler import dynProgsTSP as dynProgs

class solver(object):

    def __init__(self,dynProgs):
        self.instance = dynProgs

    def dynProgSol(self):
        '''
        prohibitive complexity ~ O(n^2 * 2^n)
        A memoized state-space search using DP
        BFS scheme
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
        G = self.instance.getCost()
        G = G + np.where(np.eye(self.instance.size) > 0, np.inf, 0)
        for i in range(self.instance.size):
            memo[(tuple({i}), i)] = G[0, i]
            P[(tuple({i}), i)] = 0
        for k in tqdm(range(2, self.instance.size + 1)):
            if k < self.instance.size:
                for aset in choiceGen(list(range(1,self.instance.size)), k):
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
                aset = list(range(self.instance.size))
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
        return memo[(tuple(list(range(self.instance.size))), 0)], pathGen(P, self.instance.size)

    def dynProgWithDng(self,delta=6):
        '''
        Dng-relaxed state space
        Paper requires delta = 8,10 for relaxation to be tight
        '''

        def nearestNeighbors(self,d=delta):
            '''
            ~ n^2 * log(n)
            '''
            C = self.instance.getCost()
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
        G = self.instance.getCost()
        G = G + np.where(np.eye(self.instance.size) > 0, np.inf, 0)
        N = nearestNeighbors(self.instance)
        NG = set(range(self.instance.size))
        for i in range(self.instance.size):
            memo[(NG,self.instance.size,i)] = sum(functionEval(NG,self.instance.size,i,memo,G))
        print(memo)

'''
solvInst = solver(dynProgs("gr17"))
print(solvInst.dynProgSol())
'''