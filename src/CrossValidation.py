'''
Created on Feb 9, 2014

@author: Jas
'''
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
class CrossValidation:
    '''
    This allows us to perform Leave-One-Out Cross Validation over
    RKHSN1
    '''
    def LOOEGenerator(self):
        '''
        description: creates the eigenvectors and diagonal matrix of eigenvalues for each matrix
        '''
        M = self.gridSize
        identityMatrix = matrix.identity(M)
        looeList = list()
        for L in self.lambdas:
            for Q in self.QN1:
                G = Q[0] + L * identityMatrix
                diagonalEigenvalues, eigenvectorMatrix = G.eigenmatrix_right()
                gInverse = EigenInverse(eigenvectorMatrix,diagonalEigenvalues,L,M)
                c = gInverse * self.Y
                D = gInverse.diagonal()
                LOOE = vector([c[i]/D[i] for i in range(len(c))])
                looeList.append((L,Q,LOOE.norm(),c))
        sortedLooeList = sorted(looeList,key=lambda d: d[2])
        return sortedLooeList
            
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
        self.gridPoints = FZ.GetGridInverseStandardDeviation()
        self.gridSize = len(self.gridPoints)
        self.taus = range(1,10)#1,2,...,9
        self.lambdas = srange(.1,10,.75)
        self.QN1 = [(matrix(RR, self.gridPoints, self.gridPoints, lambda i,j: RKHSN1(self.a,self.b,self.gridPoints[i],self.gridPoints[j],tau),tau) for tau in self.taus)]
        self.Y = vector([P[1] for P in self.gridPoints])
        self.looeListSorted= self.LOOEGenerator()
        self.L = self.looeListSorted[0][0]
        self.tau = self.looeListSorted[0][1][1]
        self.ChosenRKHSN1 = self.looeListSorted[0][1][0]
        self.c = self.looeListSorted[0][3]