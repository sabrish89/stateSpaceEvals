import numpy as np
from scipy.sparse.csgraph import minimum_spanning_tree, connected_components
from instanceHandler import dynProgsTSP as tsp

def kruskalsTree(G,inclnSet=[],exclnSet=[]):
    '''
    Manipulate G and re-use mst from scipy
    Kruskal terminates at |E| = |V|-1 edges. So multiple components not possible!
    :param G: Distance matrix
    :param inclnSet: edges that must be included
    :param exclnSet: edges that must be excluded
    :return: mst
    '''

    if type(G) == np.ndarray:
        for edge in inclnSet:
            G[edge[0], edge[1]] = G[edge[0], edge[1]] = 0
        for edge in exclnSet: #excln must override incln - design choice
            G[edge[0], edge[1]] = G[edge[0], edge[1]] = np.inf

    T = minimum_spanning_tree(G)
    n_comp, labels = connected_components(T,return_labels = True)
    if n_comp > 1:
        print("Kruskal gave connected components!")
        exit()
    else: #bild the edgeset
        mst = T.toarray(int)
        return [(i,j) for j in range(mst.shape[0]) for i in range(mst.shape[0]) if mst[i,j] > 0]

def minSpan1Tree(G):
    '''
    Min-Spanning 1 tree using kruskals algorithm
    :param G: Graph
    :return: mincost edge set for 1-tree with last two edges denoting appendix node edges
    '''

    N = G.shape[0]
    bestCost = np.inf
    bestEdgeSet = []
    for i in range(N):
        tG = np.delete(G,i,0)
        tG = np.delete(tG,i,1)
        edgeSet = [(t[0]+int(t[0]>=i),t[1]+int(t[1]>=i)) for t in kruskalsTree(tG)]
        edgeSet += [(i,np.where(val == G[:,i])[0][0]) for val in sorted(G[:,i])[1:3]]
        currCost = sum(G[edge[0], edge[1]] for edge in edgeSet)
        if currCost < bestCost:
            bestEdgeSet = edgeSet
            bestCost = currCost
    return bestEdgeSet

def generate(G,edgeSet):
    '''
    Generate children for parent edgeSet with inclusion and exclusion edge sets
    :param G: Graph Matrix
    :param edgeSet: Parent subproblem
    :return: children edgesets using inclusion and exclusion sets
    '''

    def chooseVertex(edgeSet):
        '''
        Choose a vertex
        :param edgeSet: Parent subproblem
        :return: a fuckin' vertex dammit!
        '''

        flattenedEdgeSet = [t for tup in edgeSet for t in tup]
        vrtxCard = {vrtx:flattenedEdgeSet.count(vrtx) for vrtx in flattenedEdgeSet}
        return max(vrtxCard, key=lambda key: vrtxCard[key])

    cEdgeSet = []
    vertex = chooseVertex(edgeSet)
    principEdges = [edge for edge in edgeSet if vertex in edge]
    for pEdge in principEdges:
        cEdgeSet.append(kruskalsTree(G,principEdges,[pEdge]))
    return cEdgeSet

inst = tsp("burma14")
parentProblem = minSpan1Tree(inst.getCost())
print(parentProblem)
print(generate(inst.getCost(),parentProblem))