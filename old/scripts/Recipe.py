'''
Created on Oct 31, 2013

@author: Jas
'''

class Recipe(object):
    '''
   Input: T = Time from[0,T] which is for a day each mintue (60*n)
          S = Stock prices
          x = Grid Points
          h_n = 1/n^(1/3)
          n = Number of stock data points
   Description : sigma i =1,n-1 1_{|s_t(i)-x)| < h_n} = *
   Recipe: step1: We run each stock price S_(ti) from * for each grid point x
           step 2: If * is true then we add data point in grid 
           step 3: we will have total data points in each grid 
           step 4: if each grid points have 1 or more than 1 data points we use the grid points otherwise reject it
 
    '''


    def __init__(selfparams):
        '''
        Constructor
        '''
        