'''
Created on Oct 27, 2013

@author: Jas
'''
from sage.all import *
class AssetBubble(object):
    '''
    Deciding whether and extrapolation is required
    '''

    def __init__(self,FlorenZmirouObject):
        '''
        Input: FloremZmirouObject= FlorenZmirou Class
        Discription: Step1: Determines if Extrapolation is needed
                     Step2: If true Then Extrapolate
                     Step3: Determine if asset is bubble
        '''
        self.FlorenZmirou = FlorenZmirouObject
        
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
    def ReproducingKernalFunction(self,en,m,x,y):
        '''
        Input: en,m = nth and mth derivatives
               x,y = Grid Points
        Output: Proposition 2 Reproducing Kernal function
        Description: Returns Reproducing kernal function
        '''
        xLarge = max([x,y])# maximum value of grid points (x,y)
        xSmall = min([x,y])# minimum value of grid points (x,y)
        nSquared = en*en
        coeficient2 = xLarge**(-m-1)
        BetaValue = self.BetaFunction(m+1, en)
        a = float(-en+1)
        b = float(m+1)
        c = float(en+m+1)
        z = float(xSmall/xLarge)
        GaussValue = self.HyperGeometricFunction(a,b,c,z)
        return nSquared*coeficient2*BetaValue*GaussValue
        
        