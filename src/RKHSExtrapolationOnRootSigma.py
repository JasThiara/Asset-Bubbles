'''
Created on Nov 30, 2013

@author: Jas
'''
from sage.all import *
from RKHS import RKHS
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
        2) for n = 1:
        2.1) compute matrix K1 = K^{(a,b)}_{1,tau} (x_i,x_k) where x_i, x_k are in FZ.UsableGridPoints
        2.2) K1.inverse() * f_k = C
        2.3) f^b (x) = K1(x) * C
        3) for n = 2:
        3.1) compute matrix K2 = K^{(a,b)}_{1,tau} (x_i,x_k) where x_i, x_k are in FZ.UsableGridPoints
        3.2) K2.inverse() * f_k = C
        3.3) f^b (x) = K2(x) * C
        '''
        