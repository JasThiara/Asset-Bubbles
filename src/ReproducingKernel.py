'''
Created on Nov 30, 2013

@author: Jas
'''
from sage.all import *
class ReproducingKernels(object):
    '''
    This build the Reproducing Kernels for when n=1 and n=2 referenced in "How to Detect an Asset Bubble" and found in
    "computing a family of reproducing kernels for statistical applications" by Christine Thomas-Agnan
    '''
    
    def KernelN1(self,x,y,tau):
        '''
        inputs:
        x = stock price
        y = stock price
        tau = some value
        description:
        This method is for when n = 1
        '''
        lesserValue = min([x,y])
        greaterValue = max([x,y])
        term1 = tau / sinh(tau * (self.b - self.a))
        term2 = cosh(tau*(self.b - greaterValue))
        term3 = cosh(tau*(lesserValue-self.a))
        return term1 * term2 * term3
    
    @staticmethod
    def b1(z):
        return exp(sqrt(2)*z / 2) * cos(sqrt(2)*z / 2)
    @staticmethod
    def b2(z):
        return exp(sqrt(2)*z / 2) * sin(sqrt(2)*z / 2)
    @staticmethod
    def b3(z):
        return exp(-sqrt(2)*z / 2) * cos(sqrt(2)*z / 2)
    @staticmethod
    def b4(z):
        return exp(-sqrt(2)*z / 2) * sin(sqrt(2)*z / 2)
    @staticmethod
    def delta(tau):
        term1 = tau * sqrt(2)
        term2 = sin(tau * sqrt(2)/2)*sin(tau * sqrt(2)/2)
        term3 = sinh(tau * sqrt(2)/2)*sinh(tau * sqrt(2)/2)
        return term1/(16*(term2 - term3))
    @staticmethod
    def L(tau,a1,b1,a2,b2,a3,b3,a4,a5):
        '''
        function definition from "computing a family of reproducing kernels for statistical applications" by Christine Thomas-Agnan
        
        L(tau,a1,b1,a2,b2,a3,b3,a4,a5)=:
        delta(tau) * {a1 * cos(b1 * tau * sqrt(2) +a2 * sin(b2 * tau * sqrt(2) +a3 * exp(b3 * tau * sqrt(2) + a5} + a4
        '''
        d = ReproducingKernels.delta(tau) 
        term1 = a1 * cos(b1 * tau * sqrt(2) )
        term2 = a2 * sin(b2 * tau * sqrt(2) )
        term3 = a3 * exp(b3 * tau * sqrt(2) )
        return (d * (term1 + term2 + term3 + a5) + a4)
    @staticmethod
    def EvaluateLMatrix(tau):
        LMatrix = matrix.zero(4,4)
        for i in range(0,4):
            for j in range(0,4):
                LMatrix[i,j] = ReproducingKernels.LMatrixAsFunctionalMatrix()[i,j](tau)
        return LMatrix
    
    @staticmethod
    def LMatrixAsFunctionalMatrix():
        c = sqrt(2)/4
        return [
                            [
                            lambda tau: ReproducingKernels.L(tau,-1, 1, 1, 1, 3,-1, 0,-2),#l11
                            lambda tau: ReproducingKernels.L(tau,-1, 1,-1, 1, 1,-1, 0,00),#l12
                            lambda tau: ReproducingKernels.L(tau,-1, 1, 3, 1,-1, 1, 0, 2),#l13
                            lambda tau: ReproducingKernels.L(tau,-3, 1,-1, 1,-1, 1, 0, 4) #l14
                            ],
                            [
                            lambda tau: ReproducingKernels.L(tau,-1, 1,-1, 1, 1,-1, 0,00),#l21
                            lambda tau: ReproducingKernels.L(tau, 1, 1,-1, 1, 1,-1, 0,-2),#l22
                            lambda tau: ReproducingKernels.L(tau,-1, 1, 1, 1, 1, 1, 0,00),#l23
                            lambda tau: ReproducingKernels.L(tau,-1, 1,-1, 1,-1, 1, 0, 2) #l24
                            ],
                            [
                            lambda tau: ReproducingKernels.L(tau,-1, 1, 3, 1,-1, 1,-c, 2),#l31
                            lambda tau: ReproducingKernels.L(tau,-1, 1, 1, 1, 1, 1, c,00),#l32
                            lambda tau: ReproducingKernels.L(tau, 1, 1, 1, 1,-3, 1, 0, 2),#l33
                            lambda tau: ReproducingKernels.L(tau,-1, 1, 1, 1, 1, 1, 0,00) #l34
                            ],
                            [
                            lambda tau: ReproducingKernels.L(tau,-3, 1,-1, 1,-1, 1,-c, 4),#l41
                            lambda tau: ReproducingKernels.L(tau,-1, 1,-1, 1,-1, 1,-c, 2),#l42
                            lambda tau: ReproducingKernels.L(tau,-1, 1, 1, 1, 1, 1, 0,00),#l43
                            lambda tau: ReproducingKernels.L(tau,-1, 1,-1, 1,-1, 1, 0, 2) #l44
                            ]
                           ]
    
    def KernelN2(self,x,y,tau):
        lesserValue
    def __init__(self,FZ,n,m):
        '''
        Constructor
        Inputs:
        FZ = FlorenZmirou Object
        n = as in "H_n([0,\infty[)"
        m = m <= n
        Description:
        Builds the reproducing kernels as specificed in "computing a family of reproducing kernels for statistical applications"
        for n = 1 and n=2 near equation (22) of the paper.
        '''
        self.a = FZ.Stock.minPrice
        self.b = FZ.Stock.maxPrice
        self.m = m
        self.n = n
        
        
        
        
        
        