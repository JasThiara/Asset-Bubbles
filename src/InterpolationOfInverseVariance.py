'''
Created on Nov 30, 2013

@author: Jas
'''
from sage.all import *
from RKHS import RKHS
class InterpolationOfInverseVariance(RKHS):
    '''
    This class is designed to interpolate values of 
    sigma as described in "how to detect an asset bubble" using proposition 2 and regularized methods
    '''
    @staticmethod
    def isSymmetricAndInvertible(Q):
        return Q.is_symmetric() and Q.is_invertible()
    
    def NormalizationProcedure(self):
        return self.Q.inverse() * self.F
    def RegularizationProcedure(self):
        D = self.alpha * matrix.identity(self.M,self.M)
        return (self.Q + D).inverse() * self.F
    def rkhsInterpolation(self,x):
        Q = vector(SR,self.M)
        for i in range(0,self.M):
            Q[i] = self.KernelProposition2(self.n, self.m, self.X[i],x)
        return Q * self.coefficients
    def __init__(self,FZ,n,m):
        '''
        Description:
        FZ = FlorenZmirou Object
        n  = smoothness of hilber space
        m  = m <=m
        Procedure of actions:
        Objective: Needs to find a function:
        f(x) = sum(c_i * Q(x_i,x),i,1,m)
        1) Let Q be an RKHS
        2) x_i = usable grid point
        3) sigma_k = volatility of usable grid point x_k
        4) f_k = 1/sigma_k^2
        5) if Q is symmetric, invertible
        5.1) Do normal method to solve for C_i
        5.2) Otherwise self.alpha = (m+1)/2; Do regularized method to solve for C_i
        6) Take C_i and formulate f(x)
        '''
        self.n = n
        self.m = m
        super(RKHS,self).__init__()#step 1
        self.a = FZ.Stock.minPrice
        self.b = FZ.Stock.maxPrice
        self.X = FZ.UsableGridPoints#step2
        self.M = len(self.X)
        self.F = vector(FZ.InverseVariance)#step4
        self.Q = matrix.zero(self.M,self.M)
        for i in range(0,self.M):
            for j in range(0,self.M):
                self.Q[i,j] = self.KernelProposition2(n, m, self.X[i], self.X[j])
        if InterpolationOfInverseVariance.isSymmetricAndInvertible(self.Q):
            self.coefficients = self.NormalizationProcedure()
        else:
            self.alpha = (m+1)/2
            self.coefficients = self.RegularizationProcedure()
        
        
        