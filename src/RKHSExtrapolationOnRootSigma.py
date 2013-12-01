'''
Created on Nov 30, 2013

@author: Jas
'''
from sage.all import *
from RKHS import RKHS
def frange(x, y, jump):
    l = list()
    while x < y:
        l.append(x)
        x += jump
    return l
class RKHSExtrapolationOnRootSigma(RKHS):
    '''
    classdocs
    '''


    def __init__(self,FZ):
        '''
        This performs the operations of section 5.2.3 on "how to detect an asset bubble"
        A) Non parametric estimator on sigma(x) where x is the fixed grid points -> FZ.EstimatedSigma
        B) Interpolate sigma(x) over D by 1 of 2 ways:
        B.1) cubic spline
        B.2) RKHS by lemma 10
        C) decide on extrapolation
        D) find m bar
        Input
        FZ = florenZmirou
        '''
        
        super(RKHS,self).__init__()
        #A) Non parametric estimator on sigma(x) where x is the fixed grid points -> FZ.EstimatedSigma
        #B) Interpolate sigma(x) over D by 1 of 2 ways:
        #B.1) cubic spline -> FZ.CubicInterpolatedSigma
        '''
        B.2) RKHS by lemma 10 -> DO THE FOLLOWING:
        1) f_k = 1 / sqrt(FZ.EstimatedSigma)
        2) for n = 1; tau = [1,3,6,9]:
        2.1) compute matrix K1 = K^{(a,b)}_{1,tau} (x_i,x_k) where x_i, x_k are in FZ.UsableGridPoints
        2.2) K1.inverse() * f_k = C
        2.3) f^b (x) = K1(x) * C
        3) for n = 2; tau = [1,3,6,9]:
        3.1) compute matrix K2 = K^{(a,b)}_{1,tau} (x_i,x_k) where x_i, x_k are in FZ.UsableGridPoints
        3.2) K2.inverse() * f_k = C
        3.3) f^b (x) = K2(x) * C
        '''
        self.a = FZ.Stock.minPrice
        self.b = FZ.Stock.maxPrice
        K1 = RKHSExtrapolationOnRootSigma.KernelVector()[0]#lambda a,b,x,y,tau
        K2 = RKHSExtrapolationOnRootSigma.KernelVector()[1]#lambda x,y,tau
        tau = [1,3,6,9]
        self.M = len(FZ.UsableGridPoints)
        F = vector([1/sqrt(sigma_k) for sigma_k in FZ.EstimatedSigma])#step 1
        k1Matrices = {t:matrix([[K1(self.a,self.b,x,y,t) for x in FZ.UsableGridPoints]for y in FZ.UsableGridPoints]) for t in tau}#2.1)
        k2Matrices = {t:matrix([[K2(x,y,t) for x in FZ.UsableGridPoints]for y in FZ.UsableGridPoints]) for t in tau}#3.1
        k1BasedCoefficients = {t:(M * F) for t,M in k1Matrices.iteritems()}#2.2)
        k2BasedCoefficients = {t:(M * F) for t,M in k2Matrices.iteritems()}#3.2
        k1BasedFunctions = {}
        k2BasedFunctions = {}
        for t in tau:
            k1BasedFunctions[t] = lambda x: vector([K1(self.a,self.b,xi,x,t) for xi in FZ.UsableGridPoints])*k1BasedCoefficients[t]#2.3
            k2BasedFunctions[t] = lambda x: vector([K1(self.a,self.b,xi,x,t) for xi in FZ.UsableGridPoints])*k2BasedCoefficients[t]#3.3
        
        
        
        