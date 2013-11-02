'''
Created on Oct 27, 2013

@author: Jas
'''

class GridAnalysis(object):
    '''
    Description: need to create method that determines what grid points are usable for interpolation and extrapolation 
    '''
    def GetGridPoints(self):
        '''
        Description: It will make grid Points
        Output: Returns list of grid points
        '''
        self.n = len(self.Stock.StockPrices)
        self.h_n= self.Derive_hn(self.Stock.StockPrices)
        self.T = 60*self.n # 60 sec times total number of data points because T is every minute from [0,T]
        self.x = self.Derive_x_values(self.Stock.StockPrices)

    def __init__(self,stock):
        '''
        Constructor
        '''
        self.Stock = stock
        self.GridPoints = self.GetGridPoints()
        self.UsableGridPoints= self.DoGridAnalysis()
        
    def DoGridAnalysis(self,T,S,x,n,h_n,Y):
        '''
    Input:1) T = Time from[0,T] which is for a day each mintue (60*n)
         2) S = Stock prices
         3) x = Grid Points
         4) h_n = 1/n^(1/3)
         5) n = Number of stock data points
         6) Y =  Y percent of total data points
    Ingredients: 1) S_(ti), 
                 2) indicator function, 
                 3) grid points, 
                 4) a dictionary where the keys are the grid points and the value is a list for each grid point (used in Step 2)
    Description : sigma i =1,n-1 1_{|s_t(i)-x)| < h_n} = *
    Recipe:           step1: 
                          for Si in S1,S2....Sn:
                               for x in X1,X2...Xm:
                                  if |Si-x|<h_n:
                                    step 2: 
                                    Add Si into list corresponding to x
                           Step 3:
                           for x in X1, X2,...,Xm: 
                                if the list of data points corresponding to x has greater than Y% of total grid points n:
                                     add it to the list of usable grid points
                           Step 4:
                           return the outputs
   Output: 1) the list of usable grid points
               2) for each usable grid point, the list of usable grid points
        n=len(S)
        '''
            Sum = 0.0
            for i in range len(S):
                Sti = S[i]
                for j in range of len(x):
                    xj = x[m]
                    if abs(S[i]-x[m]<h_n):
                        sum+S[i]
                    else nothing
                    
                        
                        
            
        