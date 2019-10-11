from tsplibInstanceReader import produce_matrix
from rcpsplibInstanceReader import readjslibfile

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