#coding=utf-8
'''
Created on 2016��1��12��

@author: qf
'''
from _collections import defaultdict
import math
from ensurepip import __main__
import codecs
class MaxEnt(object):
    '''
    classdocs
    '''
    
    def __init__(self):
        '''
        Constructor
        '''
        self.samples = []
        self.labels = []
        self.N = 0
        self.M = 0      #特征数量
        self.lambdas = []
        self.last_lambdas = []
        self.current_lambdas = []
        self.C = 0
        self.stepValues = [];
        self._ep_ = []  #
        self._ep = []
        self.numXY = defaultdict(int)
        self.featureId_map = {}
        self.Y = []
        
    
    def fit(self,trainX,trainY,iterNum=100):
        self.samples = trainX
        self.labels = trainY
        self.Y = set(trainY)
        self.N = len(trainY)
#         self.M = len(trainX[0])
#         self.getC()
        self.C = max([len(sample) for sample in trainX])
        for id,sample in enumerate(self.samples):
            y = self.labels[id]
            for x in set(sample):
                self.numXY[(x,y)] += 1.0
        self.M = len(self.numXY.keys())
        self.train(iterNum)

    def _EP_(self):
        
        #self._ep_ = [xyCount/self.N for xyCount in self.numXY]
        for id,xy in enumerate(self.numXY.keys()):
            self._ep_.append(self.numXY[xy]/self.N)
            self.featureId_map[xy] = id
        print len(self._ep_)
    def ZX(self,sample):
        sumY = 0.0
        for y in self.Y:
            sum = 0.0
            for x in sample:
                if self.numXY.has_key((x,y)):
                    sum += self.current_lambdas[self.featureId_map[(x,y)]]
            sumY += math.exp(sum)
                
        return sumY
                
                
    def pXY(self,sample):
        pxy = 0.0
        ZX_sum = self.ZX(sample)
        
        result = []
        for y in self.Y:
            pxy_sum = 0.0
            for x in sample:
                if self.numXY.has_key((x,y)):
                        pxy_sum += self.current_lambdas[self.featureId_map[(x,y)]]
            result.append((math.exp(pxy_sum)/ZX_sum,y))
                        
        return result
                
    def _Ep(self):   
        self._ep = [0.0]*self.M  
        for sample in self.samples:
            pxy = self.pXY(sample)
            for p,y in pxy:
                for x in sample:
                    if self.numXY.has_key((x,y)):
                        self._ep[self.featureId_map[(x,y)]] += p*1.0/self.N

    def train(self,iterNum):
        self.current_lambdas = [0.0]*self.M
        print len(self.current_lambdas)
        self._EP_()
        for iter in range(iterNum):
            #self.last_lambdas = self.current_lambdas
            self._Ep()
            for id,w in enumerate(self.current_lambdas):
#                 print id
                self.current_lambdas[id] = w + 1.0/self.C*math.log(self._ep_[id]/self._ep[id])
            print self.current_lambdas
        
    def predict(self,testX):
        X = testX
        p = self.pXY(X)
        print p
    #def predict(self,testX):
        
def loadfile():
    trainX = []
    trainY = []
    for line in codecs.open("./train",'r','utf-8').readlines():
        trainY.append(line.strip().split("\t")[0])
        trainX.append(line.strip().split("\t")[1:])
    return trainX,trainY

if __name__ == "__main__":
    maxEnt = MaxEnt()
    trainX,trainY = loadfile()
              
    maxEnt.fit(trainX,trainY,1000)
    maxEnt.predict(["sunny",    "hot",    "high",    "FALSE"])
    maxEnt.predict(["sunny",    "hot",    "high",    "True"])
    maxEnt.predict(["overcast",    "hot",    "high",    "FALSE"])###yes
    maxEnt.predict(["sunny",    "hot",    "high",    "FALSE"])
    maxEnt.predict(["sunny",    "hot",    "high",    "FALSE"])        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        