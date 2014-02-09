'''
Created on Feb 9, 2014

@author: Jas
'''
from sage.all import *
def RKHSN1(a,b,x,y,tau):
    return (tau / sinh(tau * (b - a))) * (cosh(tau*(b - max([x,y])))) * (cosh(tau*(min([x,y])-a)))
class CrossValidation:
    '''
    This allows us to perform Leave-One-Out Cross Validation over
    RKHSN1
    '''
    def EigenSpaceGenerator(self):
        '''
        '''
        id = matrix.identity(self.gridSize)
        eigenMatrices = list()
        for L in self.lambdas:
            for Q in self.QN1:
                K = Q + L * id
                eigenMatrices.append(K.eigenmatrix_right())
        return eigenMatrices
                
    def __init__(self, FZ):
        '''
        Constructor
        Input:
        Floren Zmirou Estimator - FZ
        Description:
        1) Performs LOOE over RKHSN1 on FZ  
        '''
        self.a = FZ.minPrice
        self.b = FZ.maxPrice
        self.gridPoints = FZ.GridPoints
        self.gridSize = len(self.gridPoints)
        self.taus = range(1,10)#1,2,...,9
        self.lambdas = srange(.1,10,.75)
        kernelN1 = function("kernelN1", nargs=5, eval_func=RKHSN1)
        self.QN1 = [matrix(RR, self.gridPoints, self.gridPoints, lambda i,j: kernelN1(self.a,self.b,self.gridPoints[i],self.gridPoints[j],tau) for tau in self.taus)]
        self.eigenSpaces = self.EigenSpaceGenerator()
        self.Y = FZ