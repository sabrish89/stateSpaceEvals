import numpy as np
from instanceHandler import dynProgsTSP as tsp
from branchAndBound.TSP.helpers import minSpan1Tree,generate,checkTermination
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

    def depthFirst(self, parentSet):
        '''
        depthFirst(root):
            list nodes_to_visit = {root};
            while( nodes_to_visit isn't empty ) {
              currentNode = nodes_to_visit.take_out_first();
              if( cost(currentNode) < u ) {
                if( currentNode.checkTermination() ) {
                  upperBound = currentNode.cost()
                  bestSolution = currentNode
                } else {
                  nodes_to_visit.prepend( currentNode.generate().sort() );
                }
              }
            }
        '''
        nodesToVisit = [parentSet]
        while nodesToVisit:
            currentNode = nodesToVisit.pop(0)
            if currentNode[1] < self.upperBound:
                if checkTermination(currentNode[0])[0]:
                    self.upperBound = currentNode[1]
                    self.problemSolution = currentNode[0]
                    break
                else:
                    childTemp = []
                    childrenNodes = generate(self.problemInstance.getCost(), currentNode[0][:], self.key1, currentNode[2][:])
                    for child in childrenNodes:
                        if child not in nodesToVisit and child[0].__len__() >= self.problemInstance.size:
                            childTemp.append(child)
                    nodesToVisit[0:0] = childTemp

tspInstance = tsp("burma14")
parentEdgeSet = minSpan1Tree(tspInstance.getCost())
localEdge1, localEdge2 = parentEdgeSet[0][-2:]
pivotVertex = [vertex for vertex in localEdge1 if vertex in localEdge2][0]
searchInstance = search(tspInstance)
searchInstance.key1 = pivotVertex #Use a key placeholder as pivotVertex for 1-tree
searchInstance.depthFirst(parentEdgeSet)
print(searchInstance.problemSolution,searchInstance.upperBound)