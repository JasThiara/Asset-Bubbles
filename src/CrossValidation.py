'''
Created on Feb 9, 2014

@author: Jas
'''
from sage.symbolic.function_factory import function as funky
from sage.all import *

def EigenInverse(Q,La, L,M):
    '''
    InputsL
    Q - Eigenvector Matrix -> eigenmatrix_right()
    La - diagonal matrix of eigenvalues -> eigenmatrix_right()
    L - lambda
    M - Size of Q
    Description:
    generates G inverse
    Ginv i,j = sum_{k=1}^M (Q_ik * Q_jk)/(La_kk + L)
    See "notes on regularized least squares" page 5
    '''
    doubleArray = [[sum([(Q[i,k]*Q[j,k])/(La[k,k] + L) for k in range(M)]) for i in range(M)   ] for j in range(M)  ]
    return matrix(doubleArray)
def RKHSN1(a,b,x,y,tau):
    return (tau / sinh(tau * (b - a))) * (cosh(tau*(b - max([x,y])))) * (cosh(tau*(min([x,y])-a)))
def bb(a1,a2,b1,b2,z):
    return a1 * exp(a2 * sqrt(2)*z / 2) * cos(sqrt(2)*z / 2) + b1 * exp(b2 * sqrt(2)*z / 2) * sin(sqrt(2)*z / 2)
def delta(tau):
    return tau * sqrt(2)/(16*(sin(tau * sqrt(2)/2)*sin(tau * sqrt(2)/2) - sinh(tau * sqrt(2)/2)*sinh(tau * sqrt(2)/2)))
def L(tau,a1,b1,a2,b2,a3,b3,a4,a5):
    return (delta(tau)  * (tau * sqrt(2) + a2 * sin(b2 * tau * sqrt(2) ) + a3 * exp(b3 * tau * sqrt(2) + a5) + a4))
def RKHSN2(x,y,tau):
    return L(tau,-1, 1, 1, 1, 3,-1, 0,-2) * bb(1 ,1 ,0 ,0 ,tau*min([x,y]))*bb(1 ,1 ,0 ,0 ,tau*max([x,y]))+L(tau,-1, 1,-1, 1, 1,-1, 0, 0) * bb(1 ,1 ,0 ,0 ,tau*min([x,y]))*bb(0 ,0 ,1 ,1 ,tau*max([x,y]))+L(tau,-1, 1, 3, 1,-1, 1, 0, 2) * bb(1 ,1 ,0 ,0 ,tau*min([x,y]))*bb(1 ,-1,0 ,0 ,tau*max([x,y]))+L(tau,-3, 1,-1, 1,-1, 1, 0, 4) * bb(1 ,1 ,0 ,0 ,tau*min([x,y]))*bb(0 ,0 ,1 ,-1,tau*max([x,y]))+L(tau,-1, 1,-1, 1, 1,-1, 0, 0) * bb(0 ,0 ,1 ,1 ,tau*min([x,y]))*bb(1 ,1 ,0 ,0 ,tau*max([x,y]))+L(tau, 1, 1,-1, 1, 1,-1, 0,-2) * bb(0 ,0 ,1 ,1 ,tau*min([x,y]))*bb(0 ,0 ,1 ,1 ,tau*max([x,y]))+L(tau,-1, 1, 1, 1, 1, 1, 0, 0) * bb(0 ,0 ,1 ,1 ,tau*min([x,y]))*bb(1 ,-1,0 ,0 ,tau*max([x,y]))+L(tau,-1, 1,-1, 1,-1, 1, 0, 2) * bb(0 ,0 ,1 ,1 ,tau*min([x,y]))*bb(0 ,0 ,1 ,-1,tau*max([x,y]))+L(tau,-1, 1, 3, 1,-1, 1,-sqrt(2)/4, 2) * bb(1 ,-1,0 ,0 ,tau*min([x,y]))*bb(1 ,1 ,0 ,0 ,tau*max([x,y]))+L(tau,-1, 1, 1, 1, 1, 1, sqrt(2)/4, 0) * bb(1 ,-1,0 ,0 ,tau*min([x,y]))*bb(0 ,0 ,1 ,1 ,tau*max([x,y]))+L(tau, 1, 1, 1, 1,-3, 1, 0, 2) * bb(1 ,-1,0 ,0 ,tau*min([x,y]))*bb(1 ,-1,0 ,0 ,tau*max([x,y]))+L(tau,-1, 1, 1, 1, 1, 1, 0, 0) * bb(1 ,-1,0 ,0 ,tau*min([x,y]))*bb(0 ,0 ,1 ,-1,tau*max([x,y]))+L(tau,-3, 1,-1, 1,-1, 1,-sqrt(2)/4, 4) * bb(0 ,0 ,1 ,-1,tau*min([x,y]))*bb(1 ,1 ,0 ,0 ,tau*max([x,y]))+L(tau,-1, 1,-1, 1,-1, 1,-sqrt(2)/4, 2) * bb(0 ,0 ,1 ,-1,tau*min([x,y]))*bb(0 ,0 ,1 ,1 ,tau*max([x,y]))+L(tau,-1, 1, 1, 1, 1, 1, 0, 0) * bb(0 ,0 ,1 ,-1,tau*min([x,y]))*bb(1 ,-1,0 ,0 ,tau*max([x,y]))+L(tau,-1, 1,-1, 1,-1, 1, 0, 2) * bb(0 ,0 ,1 ,-1,tau*min([x,y]))*bb(0 ,0 ,1 ,-1,tau*max([x,y]))
def RKHSM(en,m,x,y):
    return en*en * max([x,y])^(-m-1) * integrate(x^m * (1-x)**(en-1) * (1-(min([x,y])/max([x,y]))*x)**(en-1),x,0,1)   

class CrossValidationParams:
    def GetQArray(self):
        raise NotImplementedError("Implement in child class")
    def LOOEGenerator(self): 
        '''
        description: creates the eigenvectors and diagonal matrix of eigenvalues for each matrix
        '''
        M = self.gridSize
        identityMatrix = matrix.identity(M)
        looeList = list()
        for L in self.lambdas:
            for Q in self.QN:
                G = Q[0] + L * identityMatrix
                diagonalEigenvalues, eigenvectorMatrix = G.eigenmatrix_right()
                gInverse = EigenInverse(eigenvectorMatrix,diagonalEigenvalues,L,M)
                c = gInverse * self.Y
                D = gInverse.diagonal()
                LOOE = vector([c[i]/D[i] for i in range(len(c))])
                looeList.append((L,Q,LOOE.norm(),c))
        sortedLooeList = sorted(looeList,key=lambda d: d[2])
        return sortedLooeList
    
    def __init__(self,FZ,tauMin,tauMax,lambdaMin,lambdaMax,lambdaStepSize):
        self.a = FZ.minPrice
        self.b = FZ.maxPrice
        self.gridPoints = FZ.GetGridInverseStandardDeviation()
        self.gridSize = len(self.gridPoints)
        self.taus = range(1,6)#1,2,...,9
        self.lambdas = srange(.1,12,.75)
        self.QN = self.GetQArray()#[(matrix(RR, self.gridSize, self.gridSize,lambda i,j: RKHSN2(self.gridPoints[i],self.gridPoints[j],tau)),tau) for tau in self.taus]
        self.Y = vector([P[1] for P in self.gridPoints])
        self.looeListSorted= self.LOOEGenerator()
        self.L = self.looeListSorted[0][0]
        self.tau = self.looeListSorted[0][1][1]
        self.ChosenRKHSN2 = self.looeListSorted[0][1][0]
        self.c = self.looeListSorted[0][3] #needs to evaluate this with RKHSN2(self.a,self.b,self.gridPoints[i],X,tau) for any X to become an estimator
        

class CrossValidationRKHSN2(CrossValidationParams):
    '''
    This allows us to perform Leave-One-Out Cross Validation over
    RKHSN2
    '''
    def GetQArray(self):
        return [(matrix(RR, self.gridSize, self.gridSize,lambda i,j: RKHSN2(self.gridPoints[i],self.gridPoints[j],tau)),tau) for tau in self.taus]
    
    def __init__(self,FZ):
        '''
        Constructor
        Input:
        Floren Zmirou Estimator - FZ
        Description:
        1) Performs LOOE over RKHSN2 on FZ  
        '''
        CrossValidationParams.__init__(self, FZ, 1, 6, .1, 12, .75)
        
        
class CrossValidationRKHSN1(CrossValidationParams):
    '''
    This allows us to perform Leave-One-Out Cross Validation over
    RKHSN1
    '''
    def GetQArray(self):
        return [(matrix(RR, self.gridSize, self.gridSize, lambda i,j: RKHSN1(self.a,self.b,self.gridPoints[i],self.gridPoints[j],tau)),tau) for tau in self.taus]
    def __init__(self, FZ):
        '''
        Constructor
        Input:
        Floren Zmirou Estimator - FZ
        Description:
        1) Performs LOOE over RKHSN1 on FZ  
        '''
        CrossValidationParams.__init__(self, FZ, 1, 10, .1, 10, .75)

class CrossValidationRKHSM(CrossValidationParams):
    '''
    This allows us to perform Leave-One-Out Cross Validation over
    RKHSM.  However we're not sorting on min ||LOOE(RKHSM)||  we are sorting on Argmin sqrt(int(sigma_m - sigma^b))
    '''
    def GetQArray(self):
        return [(matrix(RR, self.gridSize, self.gridSize, lambda i,j: RKHSM(2,m,self.gridPoints[i],self.gridPoints[j])),m) for m in self.ems]
    def __init__(self,FZ):
        '''
        Constructor
        Input:
        Floren Zmirou Estimator - FZ
        Description:
        1) Performs LOOE over RKHSM on FZ  
        '''
        self.ems = srange(.1,10,.1) 
        CrossValidationParams.__init__(self, FZ, 1, 2, 1, 2, 1) #the last 5 entries are not important for RKHSM

class ExtrapolationOptimizationTest(CrossValidationRKHSN2):
    def ArgMinGenerator(self):
        
    def __init__(self,FZ):
        CrossValidationRKHSN2.__init__(self, FZ) 
        