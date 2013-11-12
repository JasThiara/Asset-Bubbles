'''
Created on Oct 27, 2013

@author: Jas
'''
from sage.all import *
class AssetBubble(object):
    '''
    Deciding whether and extrapolation is required
    '''
    def GetInverseVariance(self):
        '''
        Output: returns 1/sigma^2
        '''
        Sigma = self.FlorenZmirou.GetCubicInterpolatedSigma()
        Variance = Sigma*Sigma
        InverseVariance = 1/Variance
        return InverseVariance
    def __init__(self,FlorenZmirouObject):
        '''
        Input: FloremZmirouObject= FlorenZmirou Class
        Discription: Step1: Determines if Extrapolation is needed
                     Step2: If true Then Extrapolate
                     Step3: Determine if asset is bubble
        '''
        self.FlorenZmirou = FlorenZmirouObject
        self.InverseVariance = self.GetInverseVariance()
    def BetaFunction(self,m,n):
        '''
        Input: n,m = Number
        Output: Beta function Value
        Description: Returns the beta function
        '''
        return beta(m,n)
    def HyperGeometricFunction(self,a,b,c,z):
        '''
        Input: a,b,c,z
        Output: Guass's hypergeometric function
        Description: Returns Gauss's hypergeometric function 
        '''
        return maxima.hgfred([a,b],[c],z).n()
    def ReproducingKernalFunction(self,n,m,x,y):
        '''
        Input: n,m = nth and mth derivatives
               x,y = Grid Points
        Output: Proposition 2 Reproducing Kernal function
        Description: Returns Reproducing kernal function
        '''
        xLarge = max([x,y])# maximum value of grid points (x,y)
        xSmall = min([x,y])# minimum value of grid points (x,y)
        nSquared = n*n
        coeficient2 = xLarge^(-m-1)
        BetaValue = self.BetaFunction(m+1, n)
        GaussValue = self.HyperGeometricFunction(-n+1,m+1,n+m+1,xSmall/xLarge)
        return nSquared*coeficient2*BetaValue*GaussValue
        
        