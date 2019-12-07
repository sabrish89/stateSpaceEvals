import numpy as np
from instanceHandler import dynProgsTSP as tsp
from branchAndBound.TSP.helpers import kruskalsTree,span1Tree,minSpan1Tree,generate,checkTermination

class search(object):
    '''
    Implements depth-first, iterative deepening and recursive best-first
    '''
    def __init__(self,iterations = 10):
        self.iterations = iterations
