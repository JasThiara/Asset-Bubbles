'''
Created on Jan 19, 2014

@author: Jas
'''
from sage.functions.piecewise import piecewise, Piecewise 
class Spline(Piecewise):
    '''
    classdocs
    '''
    def Spline (self,pair1,pair2):
        '''
        input:
        pair1 = (xi,yi)
        pair2 = (x(i+1),y(i+1))
        output:
        q(x) for x between (xi,x(i+1)) 
        '''
        x1 = pair1[0]
        y1 = pair1[1]
        x2 = pair2[0]
        y2 = pair2[1]
        k1 =
        k2 = 
        a = k1 * (x2 - x1) - (y2-y1)
        b = -k2 * (x2 - x1) + (y2-y1)
        t = lambda x: (x - x1)/(x2 - x1)
        q = lambda x: (1-t(x)) * y1 + t(x) * (1-t(x)) * (a * (1-t(x)) + b * t(x)) 
        qPrime = lambda x: (y2-y1)/(x2-x1) + (1 - 2*t(x)) * (a * (1-t(x)) + b * t(x))/(x1-x2) +
    def __init__(self,Data):
        '''
        Constructor
        input:
        Data = [(x0,y0),(x1,y1),...,(xn,yn)]
        description:
        creates cubic spline over domain (x0,xn)
        where qi(x) is defined over (x(i-1),xi) for i=1,2,...,n
        using sage maths PieceWise class.
        '''
        