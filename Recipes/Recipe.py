'''
Created on Oct 31, 2013

@author: Jas
'''

class MyClass(object):
    '''
   Input:
          n = Number of stock data points
          m = Choice of input 
          T= Time from[0,T] which is for a day each mintue (60*n)
          infinity
    Description : We need to create two inner product functions f and g 
                step1: f = integrate(f^n(y)/n!) from 0 to infinity 
                step2: g = integrate(g^n(y)/n!) from 0 to infinity
                step3: w(y) = 1/y^m weighting function 
                step4: <f,g>n,m = integrate(f,g,w(y)) from 0 to infinity 
   Recipe: 
         step1: f= integrate(f^n(y)/n!) from 0 to infinity 
             a) Define function f
             
    '''



        