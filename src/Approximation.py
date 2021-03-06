'''
Created on Jan 4, 2014

@author: Jas
'''
from sage.all import *
from operator import itemgetter
### RKHS N=1 and N=2
from scipy import optimize
import datetime
import numpy as np

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
def MakeThirtySamples(sample):
    '''
    This is step 0
    input:
    sample = list(x1,...,xn)
    Output:
    let g = sampleSize/30
    list(
        list(x1    , x2    ,...,xg    ), #first sample
        list(x(g+1)  x(g+2),   ,x(2g) ), #second sample
        ...,
        list(x((n-1)g+1)  x((n-1)g+2),   ,xn ),#30th sample
        )
    '''
    sampleSize = len(sample)
    if sampleSize % 30 != 0:
        sampleSize = sampleSize - (sampleSize % 30) 
    return matrix(RR, 30, sample[0:sampleSize])

def BuildLOOMRKHSN1(SubSamples, a,b,tau):
    LOOMs = list()
    cols = SubSamples.ncols()
    subSampleSize = SubSamples.nrows() * SubSamples.ncols() - cols
    for i in range(30):
        rows = range(30)
        rows.remove(i)
        subSample = SubSamples[rows,0:cols].list()
        b = max(subSample)
        a = min(subSample)
        M = matrix(RR,subSampleSize,subSampleSize, lambda i,j: RKHSN1(a,b,subSample[i],subSample[j],tau))
        LOOMs.append(M)
    return LOOMs
def BuildLOOMRKHSN2(SubSamples, tau):
    LOOMs = list()
    cols = SubSamples.ncols()
    subSampleSize = SubSamples.nrows() * SubSamples.ncols() - cols
    for i in range(30):
        rows = range(30)
        rows.remove(i)
        subSample = SubSamples[rows,0:cols].list()
        M = matrix(RR,subSampleSize,subSampleSize, lambda i,j: RKHSN1(subSample[i],subSample[j],tau))
        LOOMs.append(M)
    return LOOMs
def BuildLOOMRKHSM(SubSamples, en,m):
    LOOMs = list()
    cols = SubSamples.ncols()
    subSampleSize = SubSamples.nrows() * SubSamples.ncols() - cols
    for i in range(30):
        rows = range(30)
        rows.remove(i)
        subSample = SubSamples[rows,0:cols].list()
        b = max(subSample)
        a = min(subSample)
        M = matrix(RR,subSampleSize,subSampleSize, lambda i,j: RKHSN1(en,m,subSample[i],subSample[j]))
        LOOMs.append(M)
    return LOOMs
def between(x,rangeValues):
    rangeValues.sort()#smallest->0; largest->len-1
    m = rangeValues[0]
    M = rangeValues[len(rangeValues)-1]
    return (x <= M and x >= m)
#def min(a,b):  
#    return (a + b + ((a-b)**2)**(1/2))/2
#def max(a,b):
#    return (a + b + ((a-b)**2)**(1/2))/2
def bb(a1,a2,b1,b2,z):
    return a1 * exp(a2 * sqrt(2)*z / 2) * cos(sqrt(2)*z / 2) + b1 * exp(b2 * sqrt(2)*z / 2) * sin(sqrt(2)*z / 2)
def delta(tau):
    return tau * sqrt(2)/(16*(sin(tau * sqrt(2)/2)*sin(tau * sqrt(2)/2) - sinh(tau * sqrt(2)/2)*sinh(tau * sqrt(2)/2)))
def L(tau,a1,b1,a2,b2,a3,b3,a4,a5):
    return (delta(tau)  * (tau * sqrt(2) + a2 * sin(b2 * tau * sqrt(2) ) + a3 * exp(b3 * tau * sqrt(2) + a5) + a4))
def RKHSN1(a,b,x,y,tau):
    return (tau / sinh(tau * (b - a))) * (cosh(tau*(b - max([x,y])))) * (cosh(tau*(min([x,y])-a)))
def RKHSN2(x,y,tau):
    return L(tau,-1, 1, 1, 1, 3,-1, 0,-2) * bb(1 ,1 ,0 ,0 ,tau*min([x,y]))*bb(1 ,1 ,0 ,0 ,tau*max([x,y]))+L(tau,-1, 1,-1, 1, 1,-1, 0, 0) * bb(1 ,1 ,0 ,0 ,tau*min([x,y]))*bb(0 ,0 ,1 ,1 ,tau*max([x,y]))+L(tau,-1, 1, 3, 1,-1, 1, 0, 2) * bb(1 ,1 ,0 ,0 ,tau*min([x,y]))*bb(1 ,-1,0 ,0 ,tau*max([x,y]))+L(tau,-3, 1,-1, 1,-1, 1, 0, 4) * bb(1 ,1 ,0 ,0 ,tau*min([x,y]))*bb(0 ,0 ,1 ,-1,tau*max([x,y]))+L(tau,-1, 1,-1, 1, 1,-1, 0, 0) * bb(0 ,0 ,1 ,1 ,tau*min([x,y]))*bb(1 ,1 ,0 ,0 ,tau*max([x,y]))+L(tau, 1, 1,-1, 1, 1,-1, 0,-2) * bb(0 ,0 ,1 ,1 ,tau*min([x,y]))*bb(0 ,0 ,1 ,1 ,tau*max([x,y]))+L(tau,-1, 1, 1, 1, 1, 1, 0, 0) * bb(0 ,0 ,1 ,1 ,tau*min([x,y]))*bb(1 ,-1,0 ,0 ,tau*max([x,y]))+L(tau,-1, 1,-1, 1,-1, 1, 0, 2) * bb(0 ,0 ,1 ,1 ,tau*min([x,y]))*bb(0 ,0 ,1 ,-1,tau*max([x,y]))+L(tau,-1, 1, 3, 1,-1, 1,-sqrt(2)/4, 2) * bb(1 ,-1,0 ,0 ,tau*min([x,y]))*bb(1 ,1 ,0 ,0 ,tau*max([x,y]))+L(tau,-1, 1, 1, 1, 1, 1, sqrt(2)/4, 0) * bb(1 ,-1,0 ,0 ,tau*min([x,y]))*bb(0 ,0 ,1 ,1 ,tau*max([x,y]))+L(tau, 1, 1, 1, 1,-3, 1, 0, 2) * bb(1 ,-1,0 ,0 ,tau*min([x,y]))*bb(1 ,-1,0 ,0 ,tau*max([x,y]))+L(tau,-1, 1, 1, 1, 1, 1, 0, 0) * bb(1 ,-1,0 ,0 ,tau*min([x,y]))*bb(0 ,0 ,1 ,-1,tau*max([x,y]))+L(tau,-3, 1,-1, 1,-1, 1,-sqrt(2)/4, 4) * bb(0 ,0 ,1 ,-1,tau*min([x,y]))*bb(1 ,1 ,0 ,0 ,tau*max([x,y]))+L(tau,-1, 1,-1, 1,-1, 1,-sqrt(2)/4, 2) * bb(0 ,0 ,1 ,-1,tau*min([x,y]))*bb(0 ,0 ,1 ,1 ,tau*max([x,y]))+L(tau,-1, 1, 1, 1, 1, 1, 0, 0) * bb(0 ,0 ,1 ,-1,tau*min([x,y]))*bb(1 ,-1,0 ,0 ,tau*max([x,y]))+L(tau,-1, 1,-1, 1,-1, 1, 0, 2) * bb(0 ,0 ,1 ,-1,tau*min([x,y]))*bb(0 ,0 ,1 ,-1,tau*max([x,y]))
#RKHSM
def BinomialSum(x,y,n):
    var('j')
    return sum(binomial(n,j) * x^(n-j) * y^j, j, 0, n)
def RKHSM(en,m,x,y):
    return en*en * max([x,y])^(-m-1) * integrate(x^m * (1-x)**(en-1) * (1-(min([x,y])/max([x,y]))*x)**(en-1),x,0,1)
#Q matrices by RKHS
def Q_RKHSM(en,m,data):
    Qarray = [[RKHSM(en,m,x,y) for x in data] for y in data]
    Q = matrix(Qarray)
    return Q
def Q_RKHSN1(data,a,b,tau):
    Qarray = [[RKHSN1(a,b,x,y,tau) for x in data] for y in data]
    Q = matrix(Qarray)
    return Q
def Q_RKHSN2(data,tau):
    Qarray = [[RKHSN2(x,y,tau) for x in data] for y in data]
    Q = matrix(Qarray)
    return Q
#GCV stuff
def GCV_Q_RKHSM(m,en, stockData, florenZmirouData):
    '''
    Input:
    n                     = "take the nth derivative of f"
    m                     = (integer value) "take the mth derivative of f"
    Output: 
    alpha - the estimated value needed to solve the minimization of the tikhonov regularization procedure. The regularization parameter that imposes proper balance between the residual constraint ||Qf-F|| and the magnitude constraint ||f||
    Description:
    1) Assume lambda in (0,10]
    2) G(lambda) = ||Qf - F||^2/trace(I - Q Ql)^2
    where 
    Ql = (Q.transpose() * Q + lambda^2 * I).inverse() * Q.transpose()
    and 
    f = sum(i=1,...,M) c_i^alpha Q
    where c_i^alpha are the compenents of the vector of c:
    c = (Q + lambda^2 * I).inverse() * F
    3) Interpolate G(lambda)
    4) find lambda that minimizes G(lambda)
    5) alpha = lambda^2
    '''
    #step 1
    #l = [x for x in srange(.0001,1,.0001) if x != 0]
    l = [10**(-n) for n in range(7)]
    l.extend(range(2,14,1))
    lambdaMin = 10**-6
    lambdaMax = 13
    #step 2
    Q = Q_RKHSM(en,m,stockData)
    Eye = matrix.identity(Q.nrows())
    F = vector(florenZmirouData)# F
    c = [(Q + la**2 * Eye).inverse() * F for la in l]
    f = [Q * xsi for xsi in c]
    Ql = [(Q.transpose() * Q + la**2 * Eye).inverse() * Q.transpose() for la in l]
    G = list()
    pointList = list()
    for i in range(len(l)):
        numerator = ((Q*f[i] - F).norm())**2 #||Qf - F||^2
        denomenator = ((Eye - Q * Ql[i]).trace())**2 #trace(I - Q Ql)^2
        g = numerator/denomenator
        G.append(g)
        pointList.append((l[i],g))
    #Step 3
    interpolatedG = spline(pointList)
    #Step 4
    lmin = find_root(interpolatedG.derivative,lambdaMin,lambdaMax)
    alpha = lmin**2
    #step 5
    return alpha

def GCV_Q_RKHSN1(a,b,tau, stockData, florenZmirouData):
    '''
    Input:
    n                     = "take the nth derivative of f"
    m                     = (integer value) "take the mth derivative of f"
    Output: 
    alpha - the estimated value needed to solve the minimization of the tikhonov regularization procedure. The regularization parameter that imposes proper balance between the residual constraint ||Qf-F|| and the magnitude constraint ||f||
    Description:
    1) Assume lambda in (0,10]
    2) G(lambda) = ||Qf - F||^2/trace(I - Q Ql)^2
    where 
    Ql = (Q.transpose() * Q + lambda^2 * I).inverse() * Q.transpose()
    and 
    f = sum(i=1,...,M) c_i^alpha Q
    where c_i^alpha are the compenents of the vector of c:
    c = (Q + lambda^2 * I).inverse() * F
    3) Interpolate G(lambda)
    4) find lambda that minimizes G(lambda)
    5) alpha = lambda^2
    '''
    #step 1
    #l = [x for x in srange(.0001,1,.0001) if x != 0]
    l = [10**(-n) for n in range(7)]
    l.extend(range(2,14,1))
    lambdaMin = 10**-6
    lambdaMax = 13
    #step 2
    Q = Q_RKHSN1(stockData,a,b,tau)
    Eye = matrix.identity(Q.nrows())
    F = vector(florenZmirouData)# F
    c = list()
    for la in l:
        #print "l value RKHSN1: %.11f \n"%la
        c.append((Q + la**2 * Eye).inverse() * F)
#    c = [(Q + la**2 * Eye).inverse() * F for la in l]
    f = [Q * xsi for xsi in c]
    Ql = list()
    for la in l:
        #print "l value RKHSN1: %.11f \n"%la
        A = (Q.transpose() * Q + la**2 * Eye).inverse() 
        Ql.append(A * Q.transpose())
#    Ql = [(Q.transpose() * Q + la**2 * Eye).inverse() * Q.transpose() for la in l]
    G = list()
    pointList = list()
    for i in range(len(l)):
        numerator = ((Q*f[i] - F).norm())**2 #||Qf - F||^2
        denomenator = ((Eye - Q * Ql[i]).trace())**2 #trace(I - Q Ql)^2
        g = numerator/denomenator
        G.append(g)
        pointList.append((l[i],g))
    #Step 3
    interpolatedG = spline(pointList)
    #Step 4
    lmin = find_root(interpolatedG.derivative,lambdaMin,lambdaMax)
    alpha = lmin**2
    #step 5
    return alpha

def GCV_Q_RKHSN2(tau, stockData, florenZmirouData):
    '''
    Input:
    n                     = "take the nth derivative of f"
    m                     = (integer value) "take the mth derivative of f"
    Output: 
    alpha - the estimated value needed to solve the minimization of the tikhonov regularization procedure. The regularization parameter that imposes proper balance between the residual constraint ||Qf-F|| and the magnitude constraint ||f||
    Description:
    1) Assume lambda in (0,10]
    2) G(lambda) = ||Qf - F||^2/trace(I - Q Ql)^2
    where 
    Ql = (Q.transpose() * Q + lambda^2 * I).inverse() * Q.transpose()
    and 
    f = sum(i=1,...,M) c_i^alpha Q
    where c_i^alpha are the compenents of the vector of c:
    c = (Q + lambda^2 * I).inverse() * F
    3) Interpolate G(lambda)
    4) find lambda that minimizes G(lambda)
    5) alpha = lambda^2
    '''
    #step 1
    #l = [x for x in srange(.0001,1,.0001) if x != 0]
    l = [10**(-n) for n in range(7)]
    l.extend(range(2,14,1))
    lambdaMin = 10**-6
    lambdaMax = 13
    #step 2
    Q = Q_RKHSN2(stockData,tau)
    Eye = matrix.identity(Q.nrows())
    F = vector(florenZmirouData)# F
    c = [(Q + la**2 * Eye).inverse() * F for la in l]
    f = [Q * xsi for xsi in c]
    Ql = [(Q.transpose() * Q + la**2 * Eye).inverse() * Q.transpose() for la in l]
    G = list()
    pointList = list()
    for i in range(len(l)):
        numerator = ((Q*f[i] - F).norm())**2 #||Qf - F||^2
        denomenator = ((Eye - Q * Ql[i]).trace())**2 #trace(I - Q Ql)^2
        g = numerator/denomenator
        G.append(g)
        pointList.append((l[i],g))
    #Step 3
    interpolatedG = spline(pointList)
    #Step 4
    lmin = find_root(interpolatedG.derivative,lambdaMin,lambdaMax)
    alpha = lmin**2
    #step 5
    return alpha

class Approximation(object):
    '''
    This class should be just for Interpolation and extrapolation methods.
    '''
    @staticmethod
    def RegularizedSolutionRKHSM(m,en, stockData, florenZmirouData):
        '''
        input:
        m                = m
        en               = n
        stockData        = price data (grid points)
        florenZmirouData = inverse variance from floren zmirou estimator
        output: a function f:R+ to R that is the RKHS approximation of inverse variance
        '''
        alpha = GCV_Q_RKHSM(m, en, stockData,florenZmirouData)
        Q = Q_RKHSM(en,m,stockData)
        Eye = matrix.identity(Q.nrows())
        qRegularized = Q.transpose() * Q + alpha * Eye
        c = qRegularized.inverse() * Q.transpose() * vector(florenZmirouData)
        fAlpha = lambda x: c.dot_product(vector([RKHSM(en,m,x,y) for y in stockData])) if between(x,stockData) else en*en*beta(m+1,en)*sum(c)/x**(m+1)
        return fAlpha
    @staticmethod
    def RegularizedSolutionRKHSN1(a,b,tau, stockData, florenZmirouData):
        alpha = GCV_Q_RKHSN1(a,b,tau, stockData, florenZmirouData) #replace with looms
        Q = Q_RKHSN1(stockData,a,b,tau)
        Eye = matrix.identity(Q.nrows())
        qRegularized = Q.transpose() * Q + alpha * Eye
        c = qRegularized.inverse() * Q.transpose() * vector(florenZmirouData)
        fAlpha = lambda x: c.dot_product(vector([RKHSN1(a,b,x,y,tau) for y in stockData]))
        return fAlpha
    @staticmethod
    def RegularizedSolutionRKHSN2(tau, stockData, florenZmirouData):
        '''
        REVISE THIS METHOD
        input:
        m                = m
        en               = n
        stockData        = price data (grid points)
        florenZmirouData = inverse variance from floren zmirou estimator
        output: a function f:R+ to R that is the RKHS approximation of inverse variance
        '''
        alpha = GCV_Q_RKHSN2(tau, stockData, florenZmirouData)
        m = 2 * alpha - 1#This line needs revision
        Q = Q_RKHSN2(stockData,tau)
        Eye = matrix.identity(Q.nrows())
        qRegularized = Q.transpose() * Q + alpha * Eye
        c = qRegularized.inverse() * Q.transpose() * vector(florenZmirouData)
        fAlpha = lambda x: c.dot_product(vector([RKHSN2(x,y,tau) for y in stockData])) if between(x,stockData) else 4*beta(m+1,2)*sum(c)/x**(m+1)
        return fAlpha
    
    @staticmethod
    def TauCurveFittingN1(cubicSpline,domain,FZ):
        '''
        input:
        1)cubicSpline = natural cubic spline
        2)domain = [S_min, S_max]
        3)FZ = floren Zmirou data
        output:
        1) K_(1,tau) with the best curve fit
        2) tau 
        Description:
        1) given a cubic spline, c(x)
        2) for tau = 1,...,9
        2.1) Delta_tau = (( K_(1,tau)(x) - c(x))^10)^(1/10)
        2.2) integrate Delta_tau
        2.3) Select  K_(1,tau)(x)  with the smallest Delta_tau
        '''
        a = domain[0]
        b = domain[1]
        stockData = FZ.Stock.StockPrices
        florenZmirouData = FZ.EstimatedVariance
        rkhsFunctions = [Approximation.RegularizedSolutionRKHSN1(a,b,tau, stockData, florenZmirouData) for tau in range(1,10)]
        deltaTau = list()
        var('z')
        #cubicSplineAreaUnderCurve = cubicSpline.definite_integral(a,b) <- NEEEDS REVISION
        for tau in range(1,10):
            #deltaTau.append(integrate(  ((rkhsFunctions[tau-1](z) )**2)**(1/2), (z,a,b)  )- cubicSplineAreaUnderCurve) <- NEEDS REVISION
        indexOfBestCurveFit = min(enumerate(deltaTau), key=itemgetter(1))[0] #http://stackoverflow.com/questions/13300962/python-find-index-of-minimum-item-in-list-of-floats
        tau = indexOfBestCurveFit + 1
        return Approximation.RegularizedSolutionRKHSN1(a,b,tau, stockData, florenZmirouData), tau
    @staticmethod
    def AnnealingFunction(m0,*params):
        m = m0[0]
        sigma_bSquared, a, b, en,stockData,florenZmirouData = params
        sigma_m = Approximation.RegularizedSolutionRKHSM(m,en, stockData, florenZmirouData)
        var('z')
        m_bar1 = integrate(( sigma_bSquared(z)  - sigma_m(z) )**2,(z,a,b)) 
        m_bar2 = sqrt(m_bar1)
        return m_bar2
    @staticmethod
    def TauCurveFittingN2(RKHSN1, stockData, florenZmirouData):
        '''
        find tau for RKHSN2 such that 
        objective: minimize (RKHSN1-RKHSN2)'
        '''
        taus = range(1,10)
        RKHSN2 = [Approximation.RegularizedSolutionRKHSN2(tau, stockData, florenZmirouData) for tau in taus]
        s = min(stockData)
        S = max(stockData)
        R = S-s
        h = R/100.0
        m = (RKHSN1(S) - RKHSN1(S-h))/h
        muse = [  (RKHSN2[i](S+h) - RKHSN2[i](S))/h for i in range(len(RKHSN2))   ]
        indexOfBestCurveFit = min(enumerate([(muse[i] - m) for i in range(len(RKHSN2))]), key=itemgetter(1))[0] #http://stackoverflow.com/questions/13300962/python-find-index-of-minimum-item-in-list-of-floats
        tau = indexOfBestCurveFit + 1   
        return tau
    @staticmethod
    def ArgMinM(RKHSN1, stockData, florenZmirouData):
        en = 2
        tau = Approximation.TauCurveFittingN2(RKHSN1, stockData, florenZmirouData)
        f_b = Approximation.RegularizedSolutionRKHSN2(tau, stockData, florenZmirouData)#appoximates 1/sigma^2
        sigma_bSquared = 1/f_b
        s = min(stockData)
        b = max(stockData)
        a = b - (1/3) * (b - s)
        params = (sigma_bSquared, a, b, en,stockData,florenZmirouData)
        m0 = np.array([5])
        print datetime.datetime.now()
        m_bar, argminVal,T,feval,iters,accept,status =optimize.anneal(Approximation.AnnealingFunction, m0, args=params, schedule='fast', full_output=True, maxiter=5, lower=.001,upper=10, dwell=10, disp=False)
        print datetime.datetime.now()
        return (m_bar, argminVal,T,feval,iters,accept,status,f_b)
    def __init__(self):
        '''
        Constructor
        Interpolation:
        1) over RKHM -> f_m
        2) over RKHN1 -> f_b
        Extrapolation
        3) over RKHM using proposition 3 ->f_m
        4) over RKHSN2 -> f_b
        '''
        pass