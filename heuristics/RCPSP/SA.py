import numpy as np
import math
from tqdm import tqdm
from LBs.RCPSP.precedenceDFS import getPrecedenceLB
from instanceHandler import dynProgsPSP as dynProgs


def SAHeuristic(dynProgs, parameters):
    '''
    :input parameters: [N_0,h,T_max,a,S,C]
    :return: hopefully optimal x
    '''

    def generateNeighbor(x, u, self):
        '''
        Return a random flip
        :param x: schedule scheme
        :param t: time scheme
        :param self: psp instance
        :return:
        '''


        def getT(x, self):
            '''
            Get time index for x
            :param x:
            :param self:
            :return:
            '''

            t = [0]
            for job in x:
                if job > 1:
                    T = 0
                    predecessors = [key for key in self._successors.keys() if job in self._successors[key]]
                    while True:
                        if all([t.__len__() > x.index(pjob) for pjob in predecessors]):
                            if max([t[x.index(pjob)] + self._processingTime[pjob] for pjob in x[:t.__len__()] if pjob in predecessors], default=T) <= T:
                                running = [ajob for ajob in x[:t.__len__()] if t[x.index(ajob)] < T + self._processingTime[job] + 1 and t[x.index(ajob)] + self._processingTime[ajob] > T - 1]
                                resCheckRes = [sum([self._resourceReq[compJob][r] for compJob in running if not compJob == job] + [self._resourceReq[job][r]]) <= self._resourceCap[r] for r in range(self._resourceCap.__len__())]
                                if resCheckRes == [True] * resCheckRes.__len__():
                                    t.append(T)
                                    break
                                else:
                                    T += 1
                            else:
                                T += 1
                        else:
                            print("SOMETHING WRONG!!!")
                            exit()
            return t

        x_n = x[:]
        for _ in range(np.random.randint(1, u)):
            randomJob = np.random.randint(2, x.__len__())
            idx = x_n.index(randomJob)
            predecessors = [key for key in self._successors.keys() if randomJob in self._successors[key]]
            succ_idx = min([x_n.index(j) for j in self._successors[randomJob]] + [x.__len__() - 1])
            pred_idx = max([x_n.index(j) for j in predecessors] + [0])
            if not pred_idx + 1 == succ_idx - 1:
                ogi = np.random.randint(pred_idx + 1, succ_idx - 1)
                tmp = x_n[idx]
                if idx > ogi:
                    x_n[min(idx, ogi) + 1:max(ogi, idx) + 1] = x_n[min(idx, ogi):max(ogi, idx)]
                else:
                    x_n[min(idx, ogi):max(ogi, idx)] = x_n[min(idx, ogi) + 1:max(ogi, idx) + 1]
                x_n[ogi] = tmp
                if not all(job in x_n for job in x):
                    print("CHECK HERE!")
                    exit()
        return x_n, getT(x_n, self)

    def sortByDuration(l, d):
        '''
        :param l: job dictionary
        :param d: duration dictionary
        :return: job dictionary sorted by duration dictionary
        '''

        for key in l.keys():
            ls = l[key]
            if ls.__len__() > 1:
                for idx1, job1 in enumerate(ls):
                    for idx2, job2 in enumerate(ls):
                        if idx2 > idx1:
                            if d[job2] < d[job1]:
                                ls[idx1] = job2
                                ls[idx2] = job1
                                break
        return l

    def explicitMatrixCheck(x, t, pspInstance):
        '''
        Check generated schedule as per matrix mode
        '''

        timeMatrix = np.array([[1 if time >= t[x.index(job)] and time <= t[x.index(job)] + max(pspInstance._processingTime[job]-1,0)
                       else 0 for time in range(max(t)+1)] for job in x])
        for resource in range(pspInstance._resourceCap.__len__()):
            for time in range(max(t)+1):
                if sum([pspInstance._resourceReq[job][resource] * timeMatrix[job-1][time] for job in x]) > pspInstance._resourceCap[resource]:
                    return False
        return True

    lb = getPrecedenceLB(dynProgs)
    print("Lower Bound:",lb)
    schedule = dynProgs.basicFeasible()
    inv = {}
    for key in schedule.keys():
        if schedule[key] not in inv.keys():
            inv[schedule[key]] = [key]
        else:
            inv[schedule[key]].append(key)
    sortedSchedule = sortByDuration(inv, dynProgs._processingTime)
    x_curr, t_curr = [job for key in sorted(sortedSchedule.keys()) for job in sortedSchedule[key]], \
           [t for key in sorted(sortedSchedule.keys()) for t in [key] * sortedSchedule[key].__len__()]
    x_b, t_b = x_curr, t_curr
    T = parameters[2]
    N = parameters[0]
    for s in range(parameters[4]):
        N = math.ceil(N * (1 + parameters[1] * s))
        t_prog = tqdm(range(N))
        for _ in t_prog:
            t_prog.set_description(str(s + 1) + "/" + str(parameters[4]) + " | Best:" + str(t_b[-1]))
            x_t, t_t = generateNeighbor(x_curr, s + 2, dynProgs)
            if t_t.__len__() < dynProgs._processingTime.keys().__len__():
                x_t = x_curr
                t_t = t_curr
            delta = t_t[-1] - t_curr[-1]
            if delta < 0:
                x_curr, t_curr = x_t, t_t
                if t_curr[-1] < t_b[-1]:
                    x_b = x_curr
                    t_b = t_curr
                if t_curr[-1] == lb:
                    return x_curr, t_curr
            elif np.exp(delta * -1 / T) > np.random.uniform(0, 1):
                x_curr = x_t
                t_curr = t_t
        if not explicitMatrixCheck(x_curr,t_curr,dynProgs):
            print("Violated!!!")
        T = parameters[3] * T
    return x_b, t_b

inst = dynProgs("j3013_1")
print(SAHeuristic(inst,[1000,1,60,0.25,5])) #[N_0,h,T_max,a,S,C]