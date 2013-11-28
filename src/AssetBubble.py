'''
Created on Oct 27, 2013

@author: Jas
'''
from sage.all import *

class AssetBubble(object):
    '''
    Deciding whether and extrapolation is required
    '''

    def __init__(self,FlorenZmirouObject,m,n):
        '''
        Input: 
        n                     = "take the nth derivative of f"
        FloremZmirouObject    = FlorenZmirou Class
        alpha                 = regularization parameter that imposes proper balance between the residual constraint ||Qf-F|| and the magnitude constraint ||f||
        m                     = (integer value) "take the mth derivative of f"
        Description: Step1: Determines if Extrapolation is needed
                     Step2: If true Then Extrapolate
                     Step3: Determine if asset is bubble
        '''
        self.n = n
        self.m = m
        self.alpha = float(1 + m) / 2.0
        self.FlorenZmirou = FlorenZmirouObject
        self.fAlphaCoefficients = self.RegularizedSolution(self.FlorenZmirou.InverseVariance)
        self.fAlpha = self.RegularizedInverseVariance(self.fAlphaCoefficients,m,n)
        self.extrapolatedPlotDomain, self.fExtrapolationEstimate, self.fExtrapolatedSpline = self.Proposition3(m,n)
        
        
    def RegularizedInverseVariance(self,fAlphaCoefficients,m,n):
        '''
        Input:
            fAlphaCoefficients = Coefficents solved from equation 11 in 'How to detect an asset bubble'
            m = (integer value) "take the mth derivative of f"
            n = (integer value) "take the nth derivative of f"
        Output:
            fAlpha = Q * c
        Description:
        Computes equation (10) in 'how to detect an asset bubble'
        '''
        QArray = [[self.ReproducingKernalFunction(n,m,x,y) for x in self.FlorenZmirou.UsableGridPoints] for y in self.FlorenZmirou.UsableGridPoints]
        Q = matrix(QArray)
        fAlpha = Q * fAlphaCoefficients
        return fAlpha
    
    def RegularizedSolution(self,f):
        '''
        Input:
        f = inverse variance
        alpha = regularization parameter that imposes proper balance between the residual constraint ||Qf-F|| and the magnitude constraint ||f||
        m = (integer value) "take the mth derivative of f"
        n = (integer value) "take the nth derivative of f"
        Output:
        c_i^\alpha = the coefficients of equation (10) in "how to detect an asset bubble"
        Description:
        Solves c_alpha found in equation (11) in 'how to detect an asset bubble'
        '''
        QArray = [[self.ReproducingKernalFunction(self.n,self.m,x,y) for x in self.FlorenZmirou.UsableGridPoints] for y in self.FlorenZmirou.UsableGridPoints]
        Q = matrix(QArray)
        identityMatrix = matrix.identity(Q.nrows())
        QAlphaM = Q + self.alpha * identityMatrix
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
    
    def ExtrapolatedfAlpha(self,fAlphaCoefficients,xMin,xMax,xStepSize,m,n):
        '''
        input:
        1) fAlphaCoefficients - c_i^\alpha for i = 1,...,M; M is the number of grid points
        2) xMin - the first point of extrapolation
        3) xMax - the last point of extrapolation
        4) xStepSize - step size of the domain [xMin,xMax]
        5) m - one of the smoothness paramters.
        6) n - H_n = {f in C^n ([0,infinity)) | lim_{x-> infinity} x^k * f(k)(x) = 0, for all k in [1,n-1]}
        output:
        a list of points evaluated:
        (sum_{i=1}^M c_i^\alpha )  * n^2 * B(m+1,n)
        -------------------------------------------
                            x^(m+1)
        description: performs f_\alpha (x) extrapolation on [xMin,xMax].  See Proposition 3 of 'How to detect an asset bubble'
        '''
        fAlphaCoefficientSum = sum(fAlphaCoefficients)
        nSquared = n*n
        betaValue = self.BetaFunction(m+1, n)
        xValues = self.frange(xMin, xMax, xStepSize)
        fValues = [(fAlphaCoefficientSum * nSquared * betaValue) / x**(m+1) for x in xValues]
        return fValues
        
    def Prosition3(self,m,n):
        '''
        input:
        m = mth derivative
        n = nth derivative
        output:
        1)    a vector of extrapolated values based on Proposition 3 of "how to detect asset bubbles"
              vector is f_alpha (x) for x in srange(maxPrice, maxPrice + priceRange,h_n)
        2)    A spline based off of output (1), i.e. spline( (x,f_alpha(x)) for x in srange(maxPrice, maxPrice + priceRange,h_n))
        '''
        nSquare = n * n
        betaValue = self.BetaFunction(m+1, n)
        sumCoefficients = sum(self.fAlphaCoefficients)
        constant = nSquare * betaValue * sumCoefficients
        #if the interpolated range, [a,b], the extrapolated range is [b, b + (b-a)]:
        minPrice = self.FlorenZmirou.Stock.minPrice
        maxPrice = self.FlorenZmirou.Stock.maxPrice
        priceRange = maxPrice - minPrice
        h_n = self.FlorenZmirou.h_n
        extrapolatedDomain = [x for x in srange(maxPrice, maxPrice + priceRange,h_n)]
        extrapolatedDomainPlotRange = (min(extrapolatedDomain), max(extrapolatedDomain))
        extrapolatedRange = [constant/(x**(m+1)) for x in extrapolatedDomain]
        crossProduct = list()
        for i in range(len(extrapolatedDomain)):#check if usablegridpoints is the same size as the extrapolated domain
            crossProduct.append((extrapolatedDomain[i],extrapolatedRange[i]))
        return extrapolatedDomainPlotRange,extrapolatedRange, spline(crossProduct)
    
    @staticmethod
    def frange(x, y, jump):
        l = list()
        while x < y:
            l.append(x)
            x += jump
        return l