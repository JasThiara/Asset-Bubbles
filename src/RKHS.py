'''
Created on Nov 30, 2013

@author: Jas
'''
from sage.all import *
class RKHS(object):
    '''
    This build the Reproducing Kernels for when n=1 and n=2 referenced in "How to Detect an Asset Bubble" and found in
    "computing a family of reproducing kernels for statistical applications" by Christine Thomas-Agnan
    -AND-
    the RKHS function defined in proposition 2 of "how to detect an asset by bubble"
    using the Euler Type (see: http://en.wikipedia.org/wiki/Hypergeometric_function#Euler_type )
    '''
    #Sage Expressions for Computing  RKHSN2
    max(a,b) = (a + b + ((a-b)^2)^(1/2))/2
    min(a,b) = (a + b + ((a-b)^2)^(1/2))/2
    bb(a1,a2,b1,b2,z) = a1 * exp(a2 * sqrt(2)*z / 2) * cos(sqrt(2)*z / 2) + b1 * exp(b2 * sqrt(2)*z / 2) * sin(sqrt(2)*z / 2)
    delta(tau) = tau * sqrt(2)/(16*(sin(tau * sqrt(2)/2)*sin(tau * sqrt(2)/2) - sinh(tau * sqrt(2)/2)*sinh(tau * sqrt(2)/2)))
    L(tau,a1,b1,a2,b2,a3,b3,a4,a5) = (delta(tau)  * (tau * sqrt(2) + a2 * sin(b2 * tau * sqrt(2) ) + a3 * exp(b3 * tau * sqrt(2) + a5) + a4))
    
    #RKHSN1, N2
    RKHSN1(a,b,x,y,tau) = (tau / sinh(tau * (b - a))) * (cosh(tau*(b - max(x,y)))) * (cosh(tau*(min(x,y)-a)))
    @staticmethod
    def LMatrixAsFunctionalMatrix():
        c = sqrt(2)/4
        return [
                            [
                            lambda tau: RKHS.L(tau,-1, 1, 1, 1, 3,-1, 0,-2),#l11
                            lambda tau: RKHS.L(tau,-1, 1,-1, 1, 1,-1, 0, 0),#l12
                            lambda tau: RKHS.L(tau,-1, 1, 3, 1,-1, 1, 0, 2),#l13
                            lambda tau: RKHS.L(tau,-3, 1,-1, 1,-1, 1, 0, 4) #l14
                            ],
                            [
                            lambda tau: RKHS.L(tau,-1, 1,-1, 1, 1,-1, 0, 0),#l21
                            lambda tau: RKHS.L(tau, 1, 1,-1, 1, 1,-1, 0,-2),#l22
                            lambda tau: RKHS.L(tau,-1, 1, 1, 1, 1, 1, 0, 0),#l23
                            lambda tau: RKHS.L(tau,-1, 1,-1, 1,-1, 1, 0, 2) #l24
                            ],
                            [
                            lambda tau: RKHS.L(tau,-1, 1, 3, 1,-1, 1,-c, 2),#l31
                            lambda tau: RKHS.L(tau,-1, 1, 1, 1, 1, 1, c, 0),#l32
                            lambda tau: RKHS.L(tau, 1, 1, 1, 1,-3, 1, 0, 2),#l33
                            lambda tau: RKHS.L(tau,-1, 1, 1, 1, 1, 1, 0, 0) #l34
                            ],
                            [
                            lambda tau: RKHS.L(tau,-3, 1,-1, 1,-1, 1,-c, 4),#l41
                            lambda tau: RKHS.L(tau,-1, 1,-1, 1,-1, 1,-c, 2),#l42
                            lambda tau: RKHS.L(tau,-1, 1, 1, 1, 1, 1, 0, 0),#l43
                            lambda tau: RKHS.L(tau,-1, 1,-1, 1,-1, 1, 0, 2) #l44
                            ]
                           ]
    RKHSN2(x,y,tau) = L(tau,-1, 1, 1, 1, 3,-1, 0,-2) * bb(1 ,1 ,0 ,0 ,tau*min(x,y))*bb(1 ,1 ,0 ,0 ,tau*max(x,y))+L(tau,-1, 1,-1, 1, 1,-1, 0, 0) * bb(1 ,1 ,0 ,0 ,tau*min(x,y))*bb(0 ,0 ,1 ,1 ,tau*max(x,y))+L(tau,-1, 1, 3, 1,-1, 1, 0, 2) * bb(1 ,1 ,0 ,0 ,tau*min(x,y))*bb(1 ,-1,0 ,0 ,tau*max(x,y))+L(tau,-3, 1,-1, 1,-1, 1, 0, 4) * bb(1 ,1 ,0 ,0 ,tau*min(x,y))*bb(0 ,0 ,1 ,-1,tau*max(x,y))+L(tau,-1, 1,-1, 1, 1,-1, 0, 0) * bb(0 ,0 ,1 ,1 ,tau*min(x,y))*bb(1 ,1 ,0 ,0 ,tau*max(x,y))+L(tau, 1, 1,-1, 1, 1,-1, 0,-2) * bb(0 ,0 ,1 ,1 ,tau*min(x,y))*bb(0 ,0 ,1 ,1 ,tau*max(x,y))+L(tau,-1, 1, 1, 1, 1, 1, 0, 0) * bb(0 ,0 ,1 ,1 ,tau*min(x,y))*bb(1 ,-1,0 ,0 ,tau*max(x,y))+L(tau,-1, 1,-1, 1,-1, 1, 0, 2) * bb(0 ,0 ,1 ,1 ,tau*min(x,y))*bb(0 ,0 ,1 ,-1,tau*max(x,y))+L(tau,-1, 1, 3, 1,-1, 1,-sqrt(2)/4, 2) * bb(1 ,-1,0 ,0 ,tau*min(x,y))*bb(1 ,1 ,0 ,0 ,tau*max(x,y))+L(tau,-1, 1, 1, 1, 1, 1, sqrt(2)/4, 0) * bb(1 ,-1,0 ,0 ,tau*min(x,y))*bb(0 ,0 ,1 ,1 ,tau*max(x,y))+L(tau, 1, 1, 1, 1,-3, 1, 0, 2) * bb(1 ,-1,0 ,0 ,tau*min(x,y))*bb(1 ,-1,0 ,0 ,tau*max(x,y))+L(tau,-1, 1, 1, 1, 1, 1, 0, 0) * bb(1 ,-1,0 ,0 ,tau*min(x,y))*bb(0 ,0 ,1 ,-1,tau*max(x,y))+L(tau,-3, 1,-1, 1,-1, 1,-sqrt(2)/4, 4) * bb(0 ,0 ,1 ,-1,tau*min(x,y))*bb(1 ,1 ,0 ,0 ,tau*max(x,y))+L(tau,-1, 1,-1, 1,-1, 1,-sqrt(2)/4, 2) * bb(0 ,0 ,1 ,-1,tau*min(x,y))*bb(0 ,0 ,1 ,1 ,tau*max(x,y))+L(tau,-1, 1, 1, 1, 1, 1, 0, 0) * bb(0 ,0 ,1 ,-1,tau*min(x,y))*bb(1 ,-1,0 ,0 ,tau*max(x,y))+L(tau,-1, 1,-1, 1,-1, 1, 0, 2) * bb(0 ,0 ,1 ,-1,tau*min(x,y))*bb(0 ,0 ,1 ,-1,tau*max(x,y))
    #RKHSM
    
    
#    @staticmethod
#    def KernelN1(a,b,x,y,tau):
#        '''
#        "computing a family of reproducing kernels for statistical applications" by Christine Thomas-Agnan
#        inputs:
#        x = stock price
#        y = stock price
#        tau = some value
#        description:
#        This method is for when n = 1
#        '''
#        lesserValue = min([x,y])
#        greaterValue = max([x,y])
#        term1 = tau / sinh(tau * (b - a))
#        term2 = cosh(tau*(b - greaterValue))
#        term3 = cosh(tau*(lesserValue-a))
#        return term1 * term2 * term3
#    
#    @staticmethod
#    def KernelN2(x,y,tau):
#        '''
#        "computing a family of reproducing kernels for statistical applications" by Christine Thomas-Agnan
#        inputs:
#        x = stock price
#        y = stock price
#        tau = some value
#        description:
#        This method is for when n = 1
#        '''
#        lesserValue = min([x,y])
#        greaterValue = max([x,y])
#        result = 0.0
#        L = RKHS.LMatrixAsFunctionalMatrix()
#        b = RKHS.bVector()
#        for i in range(0,4):
#            for k in range(0,4):
#                result += L[i,k](tau) * b[i](tau*lesserValue)*b[k](tau*greaterValue)
#        return result
#    @staticmethod
#    def KernelProposition2(n,m,x,y):
#        '''
#        the RKHS function defined in proposition 2 of "how to detect an asset by bubble"
#        using the Euler Type (see: http://en.wikipedia.org/wiki/Hypergeometric_function#Euler_type )
#        The goal of this is to interpolate 1/sigma^2(x)
#        '''
#        term1 = n^2
#        term2 = max([x,y])^(-m-1)
#        term3 = RKHS.EulerType(m, n, min([x,y])/max([x,y]))
#        return term1 * term2 * term3
#    @staticmethod
#    def EulerType(m,n,z):
#        '''
#        the RKHS function defined in proposition 2 of "how to detect an asset by bubble"
#        using the Euler Type (see: http://en.wikipedia.org/wiki/Hypergeometric_function#Euler_type )
#        '''
#        G = RKHS.IndefiniteEulerType(m,n,z)
#        return G(1)-G(0)
#    @staticmethod
#    def IndefiniteEulerType(m,n,z):
#        return integral((1-x)^(n-1) * x^m * (1-z*x)^(n-1),x)
#    @staticmethod
#    def RKHSinnerProduct(f,g,n,m):
#        fn = f.derivative(n)
#        gn = g.derivative(n)
#        return integral((y^n * fn(y)/factorial(n))*(y^n * gn(y)/factorial(n))*(y^m),y,0,oo)
#    @staticmethod
#    def b1(z):
#        return exp(sqrt(2)*z / 2) * cos(sqrt(2)*z / 2)
#    @staticmethod
#    def b2(z):
#        return exp(sqrt(2)*z / 2) * sin(sqrt(2)*z / 2)
#    @staticmethod
#    def b3(z):
#        return exp(-sqrt(2)*z / 2) * cos(sqrt(2)*z / 2)
#    @staticmethod
#    def b4(z):
#        return exp(-sqrt(2)*z / 2) * sin(sqrt(2)*z / 2)
#    @staticmethod
#    def bVector():
#        return [
#                lambda z: RKHS.b1(z),
#                lambda z: RKHS.b2(z),
#                lambda z: RKHS.b3(z),
#                lambda z: RKHS.b4(z)
#                ]
#    @staticmethod
#    def B(z):
#        b = RKHS.bVector()
#        return vector([b[0](z),b[1](z),b[2](z),b[3](z)])
#    @staticmethod
#    def delta(tau):
#        term1 = tau * sqrt(2)
#        term2 = sin(tau * sqrt(2)/2)*sin(tau * sqrt(2)/2)
#        term3 = sinh(tau * sqrt(2)/2)*sinh(tau * sqrt(2)/2)
#        return term1/(16*(term2 - term3))
#    @staticmethod
#    def L(tau,a1,b1,a2,b2,a3,b3,a4,a5):
#        '''
#        function definition from "computing a family of reproducing kernels for statistical applications" by Christine Thomas-Agnan
#        
#        L(tau,a1,b1,a2,b2,a3,b3,a4,a5)=:
#        delta(tau) * {a1 * cos(b1 * tau * sqrt(2) +a2 * sin(b2 * tau * sqrt(2) +a3 * exp(b3 * tau * sqrt(2) + a5} + a4
#        '''
#        d = RKHS.delta(tau) 
#        term1 = a1 * cos(b1 * tau * sqrt(2) )
#        term2 = a2 * sin(b2 * tau * sqrt(2) )
#        term3 = a3 * exp(b3 * tau * sqrt(2) )
#        return (d * (term1 + term2 + term3 + a5) + a4)
#    @staticmethod
#    def EvaluateLMatrix(tau):
#        LMatrix = matrix.zero(4,4)
#        for i in range(0,4):
#            for j in range(0,4):
#                LMatrix[i,j] = RKHS.LMatrixAsFunctionalMatrix()[i,j](tau)
#        return LMatrix
    
    
    @staticmethod
    def KernelVector():
        return [
                lambda a,b,x,y,tau  : RKHS.KernelN1( a, b, x, y, tau),
                lambda x,y,tau      : RKHS.KernelN2( x, y, tau),
                lambda n,m,x,y      : RKHS.KernelProposition2( n, m, x, y)
                ]


    def __init__(self):
        '''
        Constructor
        '''
        pass