def getTree(t,prec,successors,duration,time):
    '''
    Search tree from precedence constraints
    t (int) - timestamp
    successors (dict) - successor jobs for given job
    :return: dict := {t:[j]} - for each T get possible jobs that may be scheduled hence
    Warning - recursive : set max-depth for recursion based on instance if needed - DFS
    '''

    def checkTime(job,time,t_):
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
        t_ = checkTime(job,time,t)
        if t >= t_:
            if t in time.keys():
                time[t].append(job)
            else:
                time[t] = [job]
        if prec[job]:
            getTree(t+duration[job],prec,prec[job],duration,time)
        else:
            continue

    #CLEAN UP - linear scan O(n)
    for key in time.keys():
        if not time[key]:
            time.pop(key)