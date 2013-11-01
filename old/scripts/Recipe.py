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
   Recipe: step1: We run each stock price S_(ti) from * for each grid point x.
                       a) if |S-x_i|<h_n
                               print 1
                          else 0
           step 2: Add all 1 points to list for each x_i
           step 3: Count data from step 2 for each x_i
           step 4: if the ith grid point has less than Y percent of total data points, reject the grid point
    Output: Count number of data points in each x_i
'''
    def __init__(selfparams):
        '''
        Constructor
        '''
        