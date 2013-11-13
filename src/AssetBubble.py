'''
Created on Oct 27, 2013

@author: Jas
'''
from sage.all import *
class AssetBubble(object):
    '''
    Deciding whether and extrapolation is required
    '''

    def __init__(self,FlorenZmirouObject,alpha,m):
        '''
        Input: 
        FloremZmirouObject    = FlorenZmirou Class
        alpha                 = regularization parameter that imposes proper balance between the residual constraint ||Qf-F|| and the magnitude constraint ||f||
        m                     = (integer value) "take the mth derivative of f"
        Description: Step1: Determines if Extrapolation is needed
                     Step2: If true Then Extrapolate
                     Step3: Determine if asset is bubble
        '''
        self.FlorenZmirou = FlorenZmirouObject
        self.fAlphaCoefficients = self.RegularizedSolution(self.FlorenZmirou.InverseVariance,alpha,m)
        self.fAlpha = self.RegularizedInverseVariance(self.fAlphaCoefficients,m)
        
    def RegularizedInverseVariance(self,fAlphaCoefficients,m):
        '''
        Input:
            fAlphaCoefficients = Coefficents solved from equation 11 in 'How to detect an asset bubble'
            m = (integer value) "take the mth derivative of f"
        Output:
            fAlpha = Q * c
        Description:
        Computes equation (10) in 'how to detect an asset bubble'
        '''
        QArray = [[self.ReproducingKernalFunction(2,m,x,y) for x in self.FlorenZmirou.UsableGridPoints] for y in self.FlorenZmirou.UsableGridPoints]
        Q = matrix(QArray)
        fAlpha = Q * fAlphaCoefficients
        return fAlpha
    
    def RegularizedSolution(self,f,alpha,m):
        '''
        Input:
        f = inverse variance
        alpha = regularization parameter that imposes proper balance between the residual constraint ||Qf-F|| and the magnitude constraint ||f||
        m = (integer value) "take the mth derivative of f"
        Output:
        c_i^\alpha = the coefficients of equation (10) in "how to detect an asset bubble"
        Description:
        Solves c_alpha found in equation (11) in 'how to detect an asset bubble'
        '''
        QArray = [[self.ReproducingKernalFunction(2,m,x,y) for x in self.FlorenZmirou.UsableGridPoints] for y in self.FlorenZmirou.UsableGridPoints]
        Q = matrix(QArray)
        identityMatrix = matrix.identity(Q.nrows())
        QAlphaM = Q + alpha * identityMatrix
        fVector = vector(f)
        cAlpha = QAlphaM.inverse() * fVector
        return cAlpha
    
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
        
        