'''
Created on Jan 4, 2014

@author: Jas
'''
from sage.all import *
### RKHS N=1 and N=2
def between(x,rangeValues):
    rangeValues.sort()#smallest->0; largest->len-1
    m = rangeValues[0]
    M = rangeValues[len(rangeValues)-1]
    return (x <= M and x >= m)
def min(a,b):  
    return (a + b + ((a-b)**2)**(1/2))/2
def max(a,b):
    return (a + b + ((a-b)**2)**(1/2))/2
def bb(a1,a2,b1,b2,z):
    return a1 * exp(a2 * sqrt(2)*z / 2) * cos(sqrt(2)*z / 2) + b1 * exp(b2 * sqrt(2)*z / 2) * sin(sqrt(2)*z / 2)
def delta(tau):
    return tau * sqrt(2)/(16*(sin(tau * sqrt(2)/2)*sin(tau * sqrt(2)/2) - sinh(tau * sqrt(2)/2)*sinh(tau * sqrt(2)/2)))
def L(tau,a1,b1,a2,b2,a3,b3,a4,a5):
    return (delta(tau)  * (tau * sqrt(2) + a2 * sin(b2 * tau * sqrt(2) ) + a3 * exp(b3 * tau * sqrt(2) + a5) + a4))
def RKHSN1(a,b,x,y,tau):
    return (tau / sinh(tau * (b - a))) * (cosh(tau*(b - max(x,y)))) * (cosh(tau*(min(x,y)-a)))
def RKHSN2(x,y,tau):
    return L(tau,-1, 1, 1, 1, 3,-1, 0,-2) * bb(1 ,1 ,0 ,0 ,tau*min(x,y))*bb(1 ,1 ,0 ,0 ,tau*max(x,y))+L(tau,-1, 1,-1, 1, 1,-1, 0, 0) * bb(1 ,1 ,0 ,0 ,tau*min(x,y))*bb(0 ,0 ,1 ,1 ,tau*max(x,y))+L(tau,-1, 1, 3, 1,-1, 1, 0, 2) * bb(1 ,1 ,0 ,0 ,tau*min(x,y))*bb(1 ,-1,0 ,0 ,tau*max(x,y))+L(tau,-3, 1,-1, 1,-1, 1, 0, 4) * bb(1 ,1 ,0 ,0 ,tau*min(x,y))*bb(0 ,0 ,1 ,-1,tau*max(x,y))+L(tau,-1, 1,-1, 1, 1,-1, 0, 0) * bb(0 ,0 ,1 ,1 ,tau*min(x,y))*bb(1 ,1 ,0 ,0 ,tau*max(x,y))+L(tau, 1, 1,-1, 1, 1,-1, 0,-2) * bb(0 ,0 ,1 ,1 ,tau*min(x,y))*bb(0 ,0 ,1 ,1 ,tau*max(x,y))+L(tau,-1, 1, 1, 1, 1, 1, 0, 0) * bb(0 ,0 ,1 ,1 ,tau*min(x,y))*bb(1 ,-1,0 ,0 ,tau*max(x,y))+L(tau,-1, 1,-1, 1,-1, 1, 0, 2) * bb(0 ,0 ,1 ,1 ,tau*min(x,y))*bb(0 ,0 ,1 ,-1,tau*max(x,y))+L(tau,-1, 1, 3, 1,-1, 1,-sqrt(2)/4, 2) * bb(1 ,-1,0 ,0 ,tau*min(x,y))*bb(1 ,1 ,0 ,0 ,tau*max(x,y))+L(tau,-1, 1, 1, 1, 1, 1, sqrt(2)/4, 0) * bb(1 ,-1,0 ,0 ,tau*min(x,y))*bb(0 ,0 ,1 ,1 ,tau*max(x,y))+L(tau, 1, 1, 1, 1,-3, 1, 0, 2) * bb(1 ,-1,0 ,0 ,tau*min(x,y))*bb(1 ,-1,0 ,0 ,tau*max(x,y))+L(tau,-1, 1, 1, 1, 1, 1, 0, 0) * bb(1 ,-1,0 ,0 ,tau*min(x,y))*bb(0 ,0 ,1 ,-1,tau*max(x,y))+L(tau,-3, 1,-1, 1,-1, 1,-sqrt(2)/4, 4) * bb(0 ,0 ,1 ,-1,tau*min(x,y))*bb(1 ,1 ,0 ,0 ,tau*max(x,y))+L(tau,-1, 1,-1, 1,-1, 1,-sqrt(2)/4, 2) * bb(0 ,0 ,1 ,-1,tau*min(x,y))*bb(0 ,0 ,1 ,1 ,tau*max(x,y))+L(tau,-1, 1, 1, 1, 1, 1, 0, 0) * bb(0 ,0 ,1 ,-1,tau*min(x,y))*bb(1 ,-1,0 ,0 ,tau*max(x,y))+L(tau,-1, 1,-1, 1,-1, 1, 0, 2) * bb(0 ,0 ,1 ,-1,tau*min(x,y))*bb(0 ,0 ,1 ,-1,tau*max(x,y))
#RKHSM
def BinomialSum(x,y,n):
    var('j')
    return sum(binomial(n,j) * x^(n-j) * y^j, j, 0, n)
def RKHSM(en,m,x,y):
    return en*en * max(x,y)^(-m-1) * integrate(x^m * (1-x)**(en-1) * (1-(min(x,y)/max(x,y))*x)**(en-1),x,0,1)
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
    l = [10**(-n) for n in range(11)]
    l.extend(range(2,14,1))
    lambdaMin = 10**-10
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
    l = [10**(-n) for n in range(11)]
    l.extend(range(2,14,1))
    lambdaMin = 10**-10
    lambdaMax = 13
    #step 2
    Q = Q_RKHSN1(stockData,a,b,tau)
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
    l = [10**(-n) for n in range(11)]
    l.extend(range(2,14,1))
    lambdaMin = 10**-10
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
        qRegularized = Q + alpha * Eye
        c = qRegularized.inverse() * vector(florenZmirouData)
        fAlpha = lambda x: c.dot_product(vector([RKHSM(en,m,x,y) for y in stockData])) if between(x,stockData) else en*en*beta(m+1,en)*sum(c)/x**(m+1)
        return fAlpha
    @staticmethod
    def RegularizedSolutionRKHSN1(a,b,tau, stockData, florenZmirouData):
        alpha = GCV_Q_RKHSN1(a,b,tau, stockData, florenZmirouData)
        Q = Q_RKHSN1(stockData,a,b,tau)
        Eye = matrix.identity(Q.nrows())
        qRegularized = Q + alpha * Eye
        c = qRegularized.inverse() * vector(florenZmirouData)
        fAlpha = lambda x: c.dot_product(vector([RKHSN1(a,b,x,y,tau) for y in stockData]))
        return fAlpha
    @staticmethod
    def RegularizedSolutionRKHSN2(tau, stockData, florenZmirouData):
        '''
        input:
        m                = m
        en               = n
        stockData        = price data (grid points)
        florenZmirouData = inverse variance from floren zmirou estimator
        output: a function f:R+ to R that is the RKHS approximation of inverse variance
        '''
        alpha = GCV_Q_RKHSN2(tau, stockData, florenZmirouData)
        m = 2 * alpha - 1
        Q = Q_RKHSN2(stockData,tau)
        Eye = matrix.identity(Q.nrows())
        qRegularized = Q + alpha * Eye
        c = qRegularized.inverse() * vector(florenZmirouData)
        fAlpha = lambda x: c.dot_product(vector([RKHSN2(x,y,tau) for y in stockData])) if between(x,stockData) else 4*beta(m+1,2)*sum(c)/x**(m+1)
        return fAlpha
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
        