from gurobipy import *
import numpy as np

def subProject(Y):
    '''Solves Projection LP problem using gurobipy
       Requirements: gurobipy MIP solver
                     numpy  : import numpy as np
                     Y := Binary infeasible solution - numpy array
    '''
    if type(Y) != np.ndarray:
        print("Input not a numpy array")
        return 4
    else:
        solver = Model("projector")
        X = [[solver.addVar(ub=1, name="x_" + str(i) + "_" + str(j), vtype=GRB.BINARY)
              for j in range(Y.shape[1])]
             for i in range(Y.shape[0])]

        # objective
        obj = sum([sum([((1 - 2 * Y[i][j]) * X[i][j] + Y[i][j]) for j in range(Y.shape[1])]) for i in
                   range(Y.shape[0])])
        solver.setObjective(obj)

        # constraints
        for i in range(Y.shape[0]):
            solver.addConstr(sum([X[i][j] for j in range(Y.shape[1])]) == 1)
        for j in range(Y.shape[1]):
            solver.addConstr(sum([X[i][j] for i in range(Y.shape[0])]) == 1)

        solver.optimize()
        return np.array([[X[i][j].x for j in range(Y.shape[1])] for i in range(Y.shape[0])])