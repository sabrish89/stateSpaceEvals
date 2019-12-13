import numpy as np
from instanceHandler import dynProgsTSP as tsp
from branchAndBound.TSP.helpers import minSpan1Tree,generate,checkTermination
from heuristics.TSP.simpleUpperBounds import randomPath, nearestNeighborPath
import sys

class recursionlimit:
    def __init__(self, limit):
        self.limit = limit
        self.old_limit = sys.getrecursionlimit()

    def __enter__(self):
        sys.setrecursionlimit(self.limit)

    def __exit__(self, type, value, tb):
        sys.setrecursionlimit(self.old_limit)

class search(object):
    '''
    Implements depth-first, iterative deepening and recursive best-first
    '''
    def __init__(self, instance, iterations = 10):
        self.iterations = iterations
        self.upperBound = np.inf
        self.lowerBound = np.inf
        self.problemInstance = instance
        self.problemSolution = None
        self.key1 = None
        self.key2 = None

    def traverseGraphSimple(self, parentSet, best=True):
        '''
        Space complex graph traversal
        :param parentSet: Root Node
        :param best: True if best-first (a cost sorted breadth-first), False if depth-first
        :return: your mother!!!nothing
        '''
        nodesToVisit = [parentSet]
        while nodesToVisit:
            currentNode = nodesToVisit.pop(0)
            if currentNode[1] < self.upperBound:
                if checkTermination(currentNode[0])[0]:
                    self.upperBound = currentNode[1]
                    self.problemSolution = currentNode[0]
                    if currentNode[1] < self.key2:
                        break #This shouldnt exist! Will be suboptimal or worse than heuristic
                else:
                    if self.key2 > currentNode[1]: #expand only if parent is better than heuristic cut
                        childTemp = []
                        childrenNodes = generate(self.problemInstance.getCost(), currentNode[0][:], self.key1, currentNode[2][:])
                        for child in childrenNodes:
                            if child not in nodesToVisit and child[0].__len__() >= self.problemInstance.size:
                                childTemp.append(child)
                        if best:
                            nodesToVisit[-1:-1] = childTemp
                        else:
                            nodesToVisit[0:0] = childTemp

    def recursiveBestFirst(self, parentSet):
        '''
        RBFS(n,b(n),a(n)):
            IF cost(n) > a(n):
                RETURN cost(n);
            IF n is a goal:
                EXIT with optimal goal node n;
            IF n has no children:
                RETURN infinity;
            FOR each child n_i of n
                IF cost(n) < b(n):
                    b(n) <- MAX(b(n),cost(n_i));
                ELSE:
                    b(n) <- cost(n_i);
            SORT n_i and b(n_i) in increasing order of b(n_i);
            IF only one child:
                b(n_2) <- infinity;
            WHILE b(n_1) <= a(n) and b(n_1) < infinity:
                b(n_1) <- RBFS(n_1, b(n_1), MIN(a(n),n(n_2))); ######Recurse
                INSERT n_1 and b(n_1) in sorted order;
            RETURN b(n_1)

        :param parentSet:
        :return:
        '''


tspInstance = tsp("gr17")
parentEdgeSet = minSpan1Tree(tspInstance.getCost())
localEdge1, localEdge2 = parentEdgeSet[0][-2:]
pivotVertex = [vertex for vertex in localEdge1 if vertex in localEdge2][0]
searchInstance = search(tspInstance)
searchInstance.key1 = pivotVertex #Use a key placeholder as pivotVertex for 1-tree
searchInstance.key2 = min(randomPath(tspInstance),nearestNeighborPath(tspInstance)) #Use a key placeholder as pivotVertex for 1-tree
searchInstance.depthFirst(parentEdgeSet)
print(searchInstance.problemSolution,searchInstance.upperBound)