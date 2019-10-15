from instanceHandler import dynProgsPSP as dynProgs
import time as t
import math

def getPrecedenceLB(dynProgs):
    '''
    :return: LB - precedence job requirements
    '''

    def getTree(t, prec, successors, duration, time):
        '''
        Create tree from precedence constraints
        t (int) - timestamp
        successors (dict) - successor jobs for given job
        :return: dict := {t:[j]} - for each T get possible jobs that may be scheduled hence
        Warning - recursive : set max-depth for recursion based on instance if needed - DFS
        '''

        def checkTime(job, time, t_):
            '''
            Returns nearest to start time for job
            Mandt: Needs one pass for clean up
            TODO: Costlier space complexity due to "found" indicator : Optimize
            '''
            for t in time.keys():
                if job in time[t]:
                    if t_ >= t:
                        time[t].remove(job)
                        t_ = 0
                    else:
                        t_ = t
            return t_ if time.__len__() > 0 else 0

        for job in successors:
            t_ = checkTime(job, time, t)
            if t >= t_:
                if t in time.keys():
                    time[t].append(job)
                else:
                    time[t] = [job]
            if prec[job]:
                getTree(t + duration[job], prec, prec[job], duration, time)
            else:
                continue

    time_S = t.time()
    time = {0: [1]}
    for i in dynProgs._successors.keys():
        if i in dynProgs._processingTime.keys():
            getTree(dynProgs._processingTime[i], dynProgs._successors, dynProgs._successors[i],
                    dynProgs._processingTime, time)
    # CLEAN UP + sort - linear scan O(n)
    time = {key: time[key] for key in time.keys() if time[key]}
    # Add remaining jobs not constrained to t = 0
    time[0] += [i for i in range(1, dynProgs._resourceReq.__len__()) if i not in [t for ts in time.values() for t in ts]]
    # APPENDING - linear scan O(n)
    ls = []
    for key in sorted(time.keys()):
        ls += time[key]
        time[key] = ls[:]  # Pass by value
    print("Took",math.ceil(t.time() - time_S),"seconds!!!")
    return max(time.keys())

'''
inst = dynProgs("j301_1")
print(inst.basicFeasible())
print(inst._name,":Lower Bound:",getPrecedenceLB(inst))
'''