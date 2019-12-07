import numpy as np
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

    def kruskalsMst(G):
        '''
        Had to write my own god!#@* code to add incln and avoid excln
        :param G: Graph
        :return: tree
        '''

        def unionFind(compPath, edge):
            '''
            Union-Find Compressed Path rep based cycle detection
            :param compPath: compressed path
            :param edge: incumbent edge
            :return: True if incumbent adds cycle, False otherwise
            '''

            def find(compPath, vertex):
                '''
                naive recursive search
                :param compPath: compressed path
                :param vertex: vertex needing representation set
                :return: representation set : vertex
                '''

                if compPath[vertex] > 0:
                    return find(compPath, compPath[vertex])
                else:
                    return vertex

            x = find(compPath,edge[0])
            y = find(compPath,edge[1])
            if x == y:
                return True
            else:
                compPath[x] = y
                return False

        def flattenSortArray(G,exclnSet = []):
            '''
            A stupid flattensort!
            :param G: Graph
            :param exclnSet: edges to exclude from tree
            :return: flattened and sorted list of edges
            '''
            lst = []
            for i in range(G.shape[0]):
                for j in range(i+1,G.shape[1]):
                    if (i,j) not in exclnSet:
                        if lst:
                            for k in range(lst.__len__()):
                                if G[i,j] < G[lst[k][0],lst[k][1]]:
                                    break
                        else:
                            k = 0
                        lst.insert(k+1,(i,j))
            return lst

        instCompPath = {i:-1 for i in range(G.shape[0])}
        edgeSet = flattenSortArray(G,exclnSet)

        #Append inclusions and remove exclusions
        treeMst = [edge for edge in inclnSet if not unionFind(instCompPath,edge)]

        for edge in edgeSet:
            if treeMst.__len__() < G.shape[0] - 1:
                if not unionFind(instCompPath,edge):
                    treeMst.append(edge)
            else:
                break

        return treeMst

    if type(G) == np.ndarray:
        return kruskalsMst(G)

def span1Tree(pivotVertex,G,inclnSet=[],exclnSet=[]):
    '''
    Core Procedure - modularizing for reusability
    :param pivotVertex: proposed tour start and end node
    :param G: Graph
    :param inclnSet: edges to include in edgeSet
    :param exclnSet: edges to exclude in edgeSet - overrides inclnSet
    :return: edgeSet and cost
    '''

    tG = np.delete(G, pivotVertex, 0)
    tG = np.delete(tG, pivotVertex, 1)
    inclnSet = [(t[0] - int(t[0] >= pivotVertex), t[1] - int(t[1] >= pivotVertex)) for t in inclnSet]
    exclnSet = [(t[0] - int(t[0] >= pivotVertex), t[1] - int(t[1] >= pivotVertex)) for t in exclnSet]
    edgeSet = [(t[0] + int(t[0] >= pivotVertex), t[1] + int(t[1] >= pivotVertex)) for t in kruskalsTree(tG, inclnSet, exclnSet)]
    edgeSet += [(pivotVertex, np.where(val == G[:, pivotVertex])[0][0]) for val in sorted(G[:, pivotVertex])[1:3]]
    cost = sum(G[edge[0], edge[1]] for edge in edgeSet)
    return edgeSet, cost

def minSpan1Tree(G):
    '''
    Min-Spanning 1-tree using kruskals algorithm
    :param G: Graph
    :return: mincost edge set for 1-tree with last two edges denoting appendix node edges
    '''

    N = G.shape[0]
    bestCost = np.inf
    bestEdgeSet = []
    for i in range(N):
        edgeSet, currCost = span1Tree(i,G[:,:])
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

    def chooseVertex(edgeSet, initialVertex):
        '''
        Choose a vertex
        :param edgeSet: Parent subproblem
        :return: a fuckin' vertex dammit!
        '''

        flattenedEdgeSet = [t for tup in edgeSet for t in tup]
        vrtxCard = {vrtx:flattenedEdgeSet.count(vrtx) for vrtx in flattenedEdgeSet}
        vrtxCard.pop(initialVertex)
        return max(vrtxCard, key=lambda key: vrtxCard[key])

    def getInclusionExclusion(G,edgeSet):
        '''
        Get inclusion and exclusion edge sets from candidate.
        The idea for decomposing the problem is to re-inforce the complete tour requirement at that city,
        making its degree two. This the edgeset, if has n edges must be reduced to at most two allowed and
        n-2 prohibited
        :param edgeSet: Candidate Set
        :return: inclnSet, exclnSet
        '''

        candEdges = [edgeSet[edgeIndex] for edgeIndex in np.argsort([G[e[0],e[1]] for e in edgeSet]).tolist()[:3]]
        for edge in candEdges:
            localCopy = candEdges[:]
            localCopy.remove(edge)
            yield localCopy, [edge]

    cEdgeSet = []
    localEdge1, localEdge2 = edgeSet[-2:]
    pivotVertex = [vertex for vertex in localEdge1 if vertex in localEdge2][0]
    vertex = chooseVertex(edgeSet, pivotVertex)
    principEdges = [edge for edge in edgeSet if vertex in edge and pivotVertex not in edge]
    for inclnSet,exclnSet in getInclusionExclusion(G, principEdges):
        cEdgeSet.append(span1Tree(pivotVertex,G.copy(),inclnSet,exclnSet))
    return cEdgeSet

def checkTermination(edgeSet):
    '''
    Check if a cyclic path found
    :param edgeSet: current subproblem edgeSet
    :return: True if cycle found and terminate, False otherwise
             Also the variation in degree - if that makes sense?!?!?
    '''

    flattenedEdgeSet = [t for tup in edgeSet for t in tup]
    vrtxCard = {vrtx: flattenedEdgeSet.count(vrtx) for vrtx in flattenedEdgeSet}
    return all(value == 2 for value in vrtxCard.values()), sum((val - 2)**2 for val in vrtxCard.values()) / vrtxCard.keys().__len__()


inst = tsp("burma14")
parentProblem = minSpan1Tree(inst.getCost())
childrenProblems = generate(inst.getCost(),parentProblem)
for child in childrenProblems:
    print(checkTermination(child[0]),child)