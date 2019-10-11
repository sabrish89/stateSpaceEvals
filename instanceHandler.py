from tsplibInstanceReader import produce_matrix
from rcpsplibInstanceReader import readjslibfile
import numpy as np

class dynProgsTSP(object):

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

class dynProgsPSP(object):
    '''
    TODO: add oops specific infra
    '''
    def __init__(self,name):
        self._name = name

        #instanceData
        self._successors = None
        self._resourceReq = None
        self._resourceCap = None
        self._processingTime = None

        self.parseInstance()

    def parseInstance(self):
        '''
        parse on demand from PSPLIB
        '''
        self._successors, self._resourceReq, self._resourceCap, self._processingTime = readjslibfile(self._name)

    def basicFeasible(self):
        '''
        Greedy
        Solution: dict := {job:index}
        :return: solution
        '''

        def checkSeq(j, schedule, self):
            '''
            :param j: job
            :param schedule: current solution
            :param self: psp instance
            '''

            def getPredecessors(j, self):
                '''
                :param j: job
                :param self: psp instance
                '''
                return [key for key in self._successors.keys() if j in self._successors[key]]

            pred = getPredecessors(j, self)
            for predecessor in pred:
                if schedule[predecessor] + self._processingTime[predecessor] > schedule[j]:
                    return False
            return True

        def checkRes(j, schedule, self):
            '''
            :param j: job
            :param schedule: current solution
            :param self: psp instance
            '''

            def runningJobs(t, schedule, self):
                '''
                :param t: time
                :param schedule: current solution
                :param self: psp instance
                '''

                return [job for job in schedule.keys() if schedule[job] < t + 1
                        and schedule[job] + self._processingTime[job] > t - 1]

            timeStamp = schedule[j]
            jobs = runningJobs(timeStamp, schedule, self)
            for r in range(max(self._resourceCap.__len__(), 1)):
                if sum([self._resourceReq[compJob][r] for compJob in jobs] +
                       [self._resourceReq[job][r]]) > self._resourceCap[r]:
                    return False
            return True

        t = 0
        schedule = {j: np.inf for j in range(1, self._resourceReq.__len__())}
        while np.inf in schedule.values():
            for job in schedule.keys():
                if schedule[job] > t:
                    schedule[job] = t
                    if not (checkSeq(job, schedule, self) and checkRes(job, schedule, self)):
                        schedule[job] = np.inf
                    else:
                        continue
                else:
                    continue
                t += 1
        return schedule