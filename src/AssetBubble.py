'''
Created on Oct 27, 2013

@author: Jas
'''
from sage.all import *
from Approximation import Approximation as Approx
class AssetBubble(object):
    def __init__(self,FZ):
        """
        0) Divide the Stock sample into 30 subsamples, c1, c2,..., c30
        1) Define Qi = Q(c1,c2,...,c(i-1),c(i+1),...,c30)  for i in 1,...,30
        1.1) El, Ll = eigendecomposition(Ql) #El = eigenmatrix; Ll= eigenvalue diagonal
        1.2) Glij.inverse() (lamda) = sum_{k=1}^n (Elik * Eljk)/(Llkk + lambda) for l = 1,2,....,30
        1.3) evaluate 1.2 over various lambda values with the following:
        1.3.1) find the min(LOOE)(lambda) where
        1.3.1.1) LOOE = c/diag(Gl.inverse) #element-wise division, i.e. "first element of c divided by first element of diag(Gl.inverse), second element of c divided by second element of diag(Gl.inverse), etc"
        1.3.1.2) c = Gl.inverse * F 
        """
        #New code
        
        
        #Old Code
#        self.FZ = FZ
#        cubicSpline = FZ.CubicInterpolatedVariance
#        domain = [FZ.Stock.minPrice,FZ.Stock.maxPrice]
#        stockData = FZ.Stock.StockPrices
#        florenZmirouData = FZ.InverseVariance
#        self.RKHSN1, self.tauN1 = Approx.TauCurveFittingN1(cubicSpline, domain, FZ)
#        self.PlotAssessment(FZ)
#        self.m_bar, self.argminVal,self.T,self.feval,self.iters,self.accept,self.status,self.RKHSN2 = Approx.ArgMinM(self.RKHSN1, stockData, florenZmirouData) 
#        self.RKHSM = Approx.RegularizedSolutionRKHSM(self.m_bar,2,stockData,florenZmirouData)
#        self.isBubble = self.m_bar>1#true/false
        
        
    def PlotAssessment(self,FZ):
        '''
        plots the interpolations and extrapolations of the asset
        1) plot RKHSN1, RKHSM, Cubic Spline on [Smin, Smax]
        '''
        tickerSymbol = FZ.Stock.Ticker
        domain = [FZ.Stock.minPrice,FZ.Stock.maxPrice]
        cubicSpline = FZ.CubicInterpolatedVariance
        var('x')
        plotRKHSN1 = plot(self.RKHSN1(x), (x,domain[0],domain[1]),legend_label='RKHSN1', color=(1,0,0) )
        #plotCubicSpline = plot(cubicSpline(x), (x,domain[0],domain[1]),legend_label='cubic spline', color=(0,1,0) )
        P = plotRKHSN1 #+ plotCubicSpline
        P.save(tickerSymbol + '.png')
#class AssetBubble(object):
#    '''
#    look into the following link:
#    http://www.mathworks.com/matlabcentral/fileexchange/52-regtools/content/regu/tikhonov.m
#    Deciding whether and extrapolation is required
#    '''
#    
#    def GeneralizedCrossValidation(self,m,n):
#        '''
#        Input:
#        n                     = "take the nth derivative of f"
#        m                     = (integer value) "take the mth derivative of f"
#        Output: 
#        alpha - the estimated value needed to solve the minimization of the tikhonov regularization procedure. The regularization parameter that imposes proper balance between the residual constraint ||Qf-F|| and the magnitude constraint ||f||
#        Description:
#        1) Assume lambda in (0,10]
#        2) G(lambda) = ||Qf - F||^2/trace(I - Q Ql)^2
#        where 
#        Ql = (Q.transpose() * Q + lambda^2 * I).inverse() * Q.transpose()
#        and 
#        f = sum(i=1,...,M) c_i^alpha Q
#        where c_i^alpha are the compenents of the vector of c:
#        c = (Q + lambda^2 * I).inverse() * F
#        3) Interpolate G(lambda)
#        4) find lambda that minimizes G(lambda)
#        5) alpha = lambda^2
#        '''
#        #step 1
#        #l = [x for x in srange(.0001,1,.0001) if x != 0]
#        l = [10**(-n) for n in range(11)]
#        l.extend(range(2,14,1))
#        #step 2
#        QArray = [[self.ReproducingKernalFunction(n,m,x,y) for x in self.FlorenZmirou.UsableGridPoints] for y in self.FlorenZmirou.UsableGridPoints]
#        Q = matrix(QArray)
#        Eye = matrix.identity(Q.nrows())
#        F = vector(self.FlorenZmirou.InverseVariance)# F
#        c = [(Q + la**2 * Eye).inverse() * F for la in l]
#        f = [Q * xsi for xsi in c]
#        Ql = [(Q.transpose() * Q + la**2 * Eye).inverse() * Q.transpose() for la in l]
#        G = list()
#        pointList = list()
#        for i in range(len(l)):
#            numerator = ((Q*f[i] - F).norm())**2 #||Qf - F||^2
#            denomenator = ((Eye - Q * Ql[i]).trace())**2 #trace(I - Q Ql)^2
#            g = numerator/denomenator
#            G.append(g)
#            pointList.append((l[i],g))
#        #Step 3
#        interpolatedG = spline(pointList)
#        #Step 4
#        lmin = find_root(interpolatedG.derivative,10**(-10),1)
#        alpha = lmin**2
#        #step 5
#        return alpha
#            
#        
#    def __init__(self,FlorenZmirouObject,m,n):
#        '''
#        Input: 
#        n                     = "take the nth derivative of f"
#        FloremZmirouObject    = FlorenZmirou Class
#        
#        m                     = (integer value) "take the mth derivative of f"
#        Description: Step1: Determines if Extrapolation is needed
#                     Step2: If true Then Extrapolate
#                     Step3: Determine if asset is bubble
#        '''
#        self.n = n
#        self.m = m
#        #self.alpha = float(1 + m) / 2.0
#        self.FlorenZmirou = FlorenZmirouObject
#        self.alpha = self.GeneralizedCrossValidation(m,n)
#        self.fAlphaCoefficients = self.RegularizedSolution(self.FlorenZmirou.InverseVariance)
#        self.fAlpha = self.RegularizedInverseVariance(self.fAlphaCoefficients,m,n)
#        self.extrapolatedPlotDomain, self.fExtrapolationEstimate, self.fExtrapolatedSpline = self.Proposition3(m,n)
#        
#        
#    def RegularizedInverseVariance(self,fAlphaCoefficients,m,n):
#        '''
#        Input:
#            fAlphaCoefficients = Coefficents solved from equation 11 in 'How to detect an asset bubble'
#            m = (integer value) "take the mth derivative of f"
#            n = (integer value) "take the nth derivative of f"
#        Output:
#            fAlpha = Q * c
#        Description:
#        Computes equation (10) in 'how to detect an asset bubble'
#        '''
#        QArray = [[self.ReproducingKernalFunction(n,m,x,y) for x in self.FlorenZmirou.UsableGridPoints] for y in self.FlorenZmirou.UsableGridPoints]
#        Q = matrix(QArray)
#        fAlpha = Q * fAlphaCoefficients
#        return fAlpha
#    
#    def RegularizedSolution(self,f):
#        '''
#        Input:
#        f = inverse variance
#        alpha = regularization parameter that imposes proper balance between the residual constraint ||Qf-F|| and the magnitude constraint ||f||
#        m = (integer value) "take the mth derivative of f"
#        n = (integer value) "take the nth derivative of f"
#        Output:
#        c_i^\alpha = the coefficients of equation (10) in "how to detect an asset bubble"
#        Description:
#        Solves c_alpha found in equation (11) in 'how to detect an asset bubble'
#        '''
#        QArray = [[self.ReproducingKernalFunction(self.n,self.m,x,y) for x in self.FlorenZmirou.UsableGridPoints] for y in self.FlorenZmirou.UsableGridPoints]
#        Q = matrix(QArray)
#        identityMatrix = matrix.identity(Q.nrows())
#        QAlphaM = Q + self.alpha * identityMatrix
#        fVector = vector(f)
#        cAlpha = QAlphaM.inverse() * fVector
#        return cAlpha
#    
#    def ReproducingKernalFunction(self,en,m,x,y):
#        '''
#        Input: en,m = nth and mth derivatives
#               x,y = Grid Points
#        Output: Proposition 2 Reproducing Kernal function
#        Description: Returns Reproducing kernal function
#        '''
#        xLarge = max([x,y])# maximum value of grid points (x,y)
#        xSmall = min([x,y])# minimum value of grid points (x,y)
#        nSquared = en*en
#        coeficient2 = xLarge**(-m-1)
#        var('z')
#        EulerType = integrate(z**m * (1-z)**(en-1) * (1- (xSmall/xLarge) * z),(z,0,1))
#        return nSquared*coeficient2*EulerType
#    
#    def ExtrapolatedfAlpha(self,fAlphaCoefficients,xMin,xMax,xStepSize,m,n):
#        '''
#        input:
#        1) fAlphaCoefficients - c_i^\alpha for i = 1,...,M; M is the number of grid points
#        2) xMin - the first point of extrapolation
#        3) xMax - the last point of extrapolation
#        4) xStepSize - step size of the domain [xMin,xMax]
#        5) m - one of the smoothness paramters.
#        6) n - H_n = {f in C^n ([0,infinity)) | lim_{x-> infinity} x^k * f(k)(x) = 0, for all k in [1,n-1]}
#        output:
#        a list of points evaluated:
#        (sum_{i=1}^M c_i^\alpha )  * n^2 * B(m+1,n)
#        -------------------------------------------
#                            x^(m+1)
#        description: performs f_\alpha (x) extrapolation on [xMin,xMax].  See Proposition 3 of 'How to detect an asset bubble'
#        '''
#        fAlphaCoefficientSum = sum(fAlphaCoefficients)
#        nSquared = n*n
#        betaValue = self.BetaFunction(m+1, n)
#        xValues = self.frange(xMin, xMax, xStepSize)
#        fValues = [(fAlphaCoefficientSum * nSquared * betaValue) / x**(m+1) for x in xValues]
#        return fValues
#        
#    def Proposition3(self,m,n):
#        '''
#        input:
#        m = mth derivative
#        n = nth derivative
#        output:
#        1)    a vector of extrapolated values based on Proposition 3 of "how to detect asset bubbles"
#              vector is f_alpha (x) for x in srange(maxPrice, maxPrice + priceRange,h_n)
#        2)    A spline based off of output (1), i.e. spline( (x,f_alpha(x)) for x in srange(maxPrice, maxPrice + priceRange,h_n))
#        '''
#        nSquare = n * n
#        betaValue = beta(m+1, n)
#        sumCoefficients = sum(self.fAlphaCoefficients)
#        constant = nSquare * betaValue * sumCoefficients
#        #if the interpolated range, [a,b], the extrapolated range is [b, b + (b-a)]:
#        minPrice = self.FlorenZmirou.Stock.minPrice
#        maxPrice = self.FlorenZmirou.Stock.maxPrice
#        priceRange = maxPrice - minPrice
#        h_n = self.FlorenZmirou.h_n
#        extrapolatedDomain = [x for x in srange(maxPrice, maxPrice + priceRange,h_n)]
#        extrapolatedDomainPlotRange = (min(extrapolatedDomain), max(extrapolatedDomain))
#        extrapolatedRange = [constant/(x**(m+1)) for x in extrapolatedDomain]
#        crossProduct = list()
#        for i in range(len(extrapolatedDomain)):#check if usablegridpoints is the same size as the extrapolated domain
#            crossProduct.append((extrapolatedDomain[i],extrapolatedRange[i]))
#        return extrapolatedDomainPlotRange,extrapolatedRange, spline(crossProduct)
#    
#    @staticmethod
#    def frange(x, y, jump):
#        l = list()
#        while x < y:
#            l.append(x)
#            x += jump
#        return l