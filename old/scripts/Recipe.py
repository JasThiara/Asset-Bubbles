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
    Ingredients: S_(ti), indicator function, grid points
   Description : sigma i =1,n-1 1_{|s_t(i)-x)| < h_n} = *
   Recipe: step1: for Si in S1,S2....Sn:
                  for x in X1,X2...Xm:
                        if |Si-x|<h_n
                               step 2
                          else 0
        step 4: if the ith grid point has less than Y percent of total data points, reject the grid point
   Output: Count number of data points in each x_i
'''
    def __init__(selfparams):
        '''
        Constructor
        '''
        